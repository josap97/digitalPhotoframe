import sys
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
if sys.version_info[0] == 2:  # the tkinter library changed it's name from Python 2 to 3.
    import Tkinter
    tkinter = Tkinter
else:
    import tkinter
import random
import config
import physDefinitions as pd

import numpy as np
import subprocess
import shutil

def export_bubble_video(
    bubbles,
    out_path="bubblePositionVideo.mp4",
    fps=None,
    cmap_gray=False,
    verbose=True,
):
    """
    Rasterise bubble positions and stream them to ffmpeg.

    Parameters
    ----------
    bubbles : sequence
        Objects with .posXHistory, .posYHistory (arrays) and .r (radius).
    config : object
        Needs .winwidth, .winheight, .rmax, .dt.
    out_path : str
        Output video file.
    fps : float or None
        Frames per second. Defaults to 1/config.dt.
    cmap_gray : bool
        False -> black bubbles on white (matches imshow default 'viridis'-ish look
        inverted? see notes below). True -> grayscale uint8 frames.
    verbose : bool
        Print progress.
    """
    rmax = int(config.rmax)
    W = int(config.winwidth)
    H = int(config.winheight)

    n_frames = len(bubbles[0].posXHistory)
    if fps is None:
        fps = 1.0 / config.dt

    # Pre-extract histories and radii as plain arrays (avoids attribute lookups
    # and any property overhead inside the hot loop).
    xs = [np.asarray(b.posXHistory, dtype=np.float32) for b in bubbles]
    ys = [np.asarray(b.posYHistory, dtype=np.float32) for b in bubbles]
    rs = [float(b.r) for b in bubbles]
    lastFrames = [float(b.lastFrame) for b in bubbles]

    # Precompute, per bubble, the local offsets of the disc mask and its bbox.
    # This is the key optimisation: we only touch pixels inside each bubble.
    discs = []
    for r in rs:
        ri = int(np.ceil(r))
        yy, xx = np.ogrid[-ri : ri + 1, -ri : ri + 1]
        mask = (xx * xx + yy * yy) <= r * r
        # bounding box of the mask, relative to bubble centre
        rows = np.any(mask, axis=1)
        cols = np.any(mask, axis=0)
        r0, r1 = np.where(rows)[0][[0, -1]]
        c0, c1 = np.where(cols)[0][[0, -1]]
        discs.append((mask[r0 : r1 + 1, c0 : c1 + 1], r0 - ri, c0 - ri))

    # Find ffmpeg
    ffmpeg = shutil.which("ffmpeg")
    if ffmpeg is None:
        raise RuntimeError(
            "ffmpeg not found on PATH. Install it (apt install ffmpeg / brew install ffmpeg)."
        )

    # yuv420p requires even dimensions.
    W_enc = W + (W % 2)
    H_enc = H + (H % 2)

    cmd = [
        ffmpeg,
        "-y",
        "-loglevel", "error",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-pix_fmt", "gray",           # single-channel uint8
        "-s", f"{W_enc}x{H_enc}",
        "-r", str(fps),
        "-i", "-",                    # read from stdin
        "-an",
        "-vcodec", "libx264",
        "-pix_fmt", "yuv420p",
        "-crf", "18",
        "-preset", "veryfast",
        out_path,
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)

    try:
        for i in range(n_frames-1):
            # Start with white background (255) to mimic imshow of a 0/1 map
            # where 0 is dark. Swap to np.zeros if you want black bg.
            frame = np.full((H_enc, W_enc), 255, dtype=np.uint8)

            for (mask, dr, dc), bx, by in zip(discs, xs, ys):
                cx = int(round(float(bx[i])))
                cy = int(round(float(by[i])))

                # Bubble centre in the padded coordinate system was at
                # (rmax + pos), then cropped back by rmax -> just pos.
                # So target top-left in frame coords:
                y0 = cy + dr
                x0 = cx + dc
                mh, mw = mask.shape

                # Clip to frame bounds
                fy0, fx0 = max(y0, 0), max(x0, 0)
                fy1, fx1 = min(y0 + mh, H_enc), min(x0 + mw, W_enc)
                if fy0 >= fy1 or fx0 >= fx1:
                    continue
                my0, mx0 = fy0 - y0, fx0 - x0
                my1, mx1 = my0 + (fy1 - fy0), mx0 + (fx1 - fx0)

                sub = frame[fy0:fy1, fx0:fx1]
                sub[mask[my0:my1, mx0:mx1]] = 0   # draw bubble as black

            if cmap_gray:
                pass  # already gray
            proc.stdin.write(frame.tobytes())

            if verbose and (i % 50 == 0 or i == n_frames - 1):
                print(f"\rframe {i+1}/{n_frames}", end="", flush=True)
    finally:
        if verbose:
            print()
        proc.stdin.close()
        ret = proc.wait()
        if ret != 0:
            raise RuntimeError(f"ffmpeg exited with code {ret}")

    print(f"Bubbles exported as video -> {out_path}")


#export_bubble_video(bubbles, config)