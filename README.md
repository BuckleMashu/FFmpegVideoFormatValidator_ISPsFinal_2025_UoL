# ISP's Final Exercise3

This repository contains a Python project developed as an exercise for an Intelligent Signal Processing course. It uses ffprobe (via ffmpeg-python) 
to examine video files, identify deviations from specified format guidelines, and then uses ffmpeg to convert these files to adhere to the guidelines.

The project is implemented in a Jupyter Notebook (exer3_24022025_submission_app.ipynb) and processes video files located in an Exercise3_Films directory, 
outputting converted files to Exercise3_Films_formatOK.

To run this code, you will have to create two folders (Exercise3_Films and Exercise3_Films_formatOK) and populate Exercise3_Films with mp4 of your choice.

- Project Tasks & Features:

  - Video File Examination (ffprobe):

    *Iterates through video files in a specified input directory.
    
    *Uses ffmpeg.probe() to extract detailed metadata for each video and audio stream.

  - Format Guideline Adherence Check:

    *Compares extracted metadata against a predefined set of video format guidelines, which include:

            +Video Format (Container): mp4

            +Video Codec: h.264

            +Audio Codec: aac

            +Frame Rate: 25 FPS

            +Aspect Ratio: 16:9

            +Resolution: 640x360

            +Video Bit Rate: 2 – 5 Mb/s

            +Audio Bit Rate: up to 256 kb/s

            +Audio Channels: stereo

    *Identifies which specific guidelines each video file fails to meet.

    *Generates a report (Submissions'_problems_report.txt) detailing the issues found for each non-compliant video.

  - Video Conversion (ffmpeg):

    *For files not adhering to the guidelines, dynamically constructs ffmpeg conversion commands.

    *Sets appropriate output options (e.g., -c:v libx264, -c:a aac, -r 25, -vf scale=640:360,setdar=16/9, bit rate constraints) only for the aspects that need correction.

    *Converts the non-compliant videos and saves them to an output directory with _formatOK appended to their original names (and changed to .mp4 extension).

    *Includes a final check on the converted files to verify they now meet all guidelines.

- Technologies Used:

    *Python 3

    *ffmpeg-python (wrapper for FFmpeg and FFprobe)

    *FFmpeg and FFprobe (must be installed and accessible in the system PATH)

    *os module (for file system operations)

    *fractions module (for aspect ratio calculation)

