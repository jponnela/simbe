# This program was developed from SiBe.
# It was converted to Python 3 and operators -- & --- & ---- & ----- were introduced.
#
# JP Onnela / October 3, 2015
#
# Usage: python simbe.py test.simbe

# Define SimBe special characters.
SIMBE_FRAME = "**"                              # Start new Beamber frame
SIMBE_BULLET = "-"                              # Insert bullet using itemize
SIMBE_EQN_BEGIN = "--"                          # Begin equation
SIMBE_EQN_END = "--"                            # End equation
SIMBE_EQN_END_NN = "--nn"                       # End equation with no numbering
SIMBE_FIG = "---"                               # Begin or end figure
SIMBE_CODE = "----"                             # Begin or end code (lstlisting)
SIMBE_CODE_LONG = "-----"                       # Begin or end code from file(lstinputlisting)


def read_parms():
    """ Read input file name from the user."""
    import sys
    try:
        filename = sys.argv[1]
    except:
        print("Please provide the input file name.")
        sys.exit()
    return filename

    
def read_file(inputfile):
    """ Read the lines in each frame to a frame buffer (dictionary)."""
    frames = {}
    frame_no = 0
    for line in open(inputfile):
        line = line.rstrip()
        if line[0:len(SIMBE_FRAME)] == SIMBE_FRAME:
            frame_no += 1
        try:
            frames[frame_no].append(line)
        except:
            frames[frame_no] = [line]
    return frames


def add_frames(frames, start_frame=1):
    """ Add the frame envinronments with titles."""
    for frame_no in sorted(frames.keys())[start_frame:]:
        frame_title = frames[frame_no][0][len(SIMBE_FRAME):]
        frames[frame_no][0] = "\\frametitle{" + frame_title + "}" 
        frames[frame_no].insert(0, "\\begin{frame}[fragile]")
        frames[frame_no].append("\\end{frame}")


def add_lstinputlisting_env(frames, start_frame=1):
    for frame_no in sorted(frames.keys())[start_frame:]:
        for line_no in range(len(frames[frame_no])):
            line = frames[frame_no][line_no]
            if line[:len(SIMBE_CODE_LONG)]==SIMBE_CODE_LONG and len(line)>2*len(SIMBE_CODE_LONG) and line[-len(SIMBE_CODE_LONG):] == SIMBE_CODE_LONG:
                line = line[len(SIMBE_CODE_LONG):-len(SIMBE_CODE_LONG)]
                frames[frame_no][line_no] = "\\lstinputlisting{" + line + "}"


def add_lstlisting_env(frames, start_frame=1):
    lstlisting_open = False
    for frame_no in sorted(frames.keys())[start_frame:]:
        for line_no in range(len(frames[frame_no])):
            line = frames[frame_no][line_no]
            # We have a 1-line code insertion.
            if line[:len(SIMBE_CODE)]==SIMBE_CODE and len(line)>2*len(SIMBE_CODE) and line[-len(SIMBE_CODE):] == SIMBE_CODE:
                    line = line[len(SIMBE_CODE):-len(SIMBE_CODE)]
                    frames[frame_no][line_no] = "\\begin{lstlisting}\n" + line + "\n" +  "\\end{lstlisting}\n"
            # We may have a 3-line code insertion.
            else:
                if line==SIMBE_CODE and not lstlisting_open:
                    frames[frame_no][line_no] = "\\begin{lstlisting}"
                    lstlisting_open = True
                elif line==SIMBE_CODE and lstlisting_open:
                    frames[frame_no][line_no] = "\\end{lstlisting}"
                    lstlisting_open = False


def add_figure_env(frames, start_frame=1):
    figure_open = False
    for frame_no in sorted(frames.keys())[start_frame:]:
        for line_no in range(len(frames[frame_no])):
            if frames[frame_no][line_no] == SIMBE_FIG:
                if not figure_open:
                    figure_open = True
                    frames[frame_no][line_no] = "\\begin{center}  \\begin{figure}"
                else:
                    frames[frame_no][line_no] = "\\end{figure}  \\end{center}"
                    figure_open = False
            elif figure_open and frames[frame_no][line_no][0:len(SIMBE_BULLET)] != SIMBE_BULLET:
                line = frames[frame_no][line_no]
                (figname, figsize) = line.split(",")
                frames[frame_no][line_no] = "\\includegraphics[width=" + figsize + "\\textwidth]{" + figname + "}"
            elif figure_open and frames[frame_no][line_no][0:len(SIMBE_BULLET)] == SIMBE_BULLET:
                line = frames[frame_no][line_no]
                frames[frame_no][line_no] = "\\caption{" + line[1:] + "}"


def add_equation_env(frames, start_frame=1):
    equation_open = False
    for frame_no in sorted(frames.keys())[start_frame:]:
        for line_no in range(len(frames[frame_no])):
            line = frames[frame_no][line_no]
            # We have a 1-line equation.
            if line[:len(SIMBE_EQN_BEGIN)]==SIMBE_EQN_BEGIN and len(line)>len(SIMBE_EQN_END_NN):
                if line[-len(SIMBE_EQN_END):] == SIMBE_EQN_END:
                    line = line[len(SIMBE_EQN_BEGIN):-len(SIMBE_EQN_END)]
                    frames[frame_no][line_no] = "\\begin{equation}\n" + line + "\n" +  "\\end{equation}\n"
                elif line[-len(SIMBE_EQN_END_NN):] == SIMBE_EQN_END_NN:
                    line = line[len(SIMBE_EQN_BEGIN):-len(SIMBE_EQN_END_NN)]
                    frames[frame_no][line_no] = "\\begin{equation}\n" + line + "\n" + "\\nonumber\n \\end{equation}\n"
            # We may have a 3-line equation.
            else:
                if line==SIMBE_EQN_BEGIN and not equation_open:
                    frames[frame_no][line_no] = "\\begin{equation}"
                    equation_open = True
                elif line==SIMBE_EQN_END and equation_open:
                    frames[frame_no][line_no] = "\\end{equation}"
                    equation_open = False
                elif line==SIMBE_EQN_END_NN and equation_open:
                    frames[frame_no][line_no] = "\\nonumber \\end{equation}"
                    equation_open = False


def add_itemize_env(frames, start_frame=1):
    """ Add the itemize environments."""
    for frame_no in sorted(frames.keys())[start_frame:]:
        frame = frames[frame_no]
        new_frame = []
        bullet_depth = 0
        for line_no in range(len(frame)):
            if line_no == 0:
                new_frame.append(frame[line_no])
            elif line_no > 0:
                # Locate bullet depth.
                if frame[line_no][0:len(SIMBE_BULLET)] == SIMBE_BULLET and frame[line_no][len(SIMBE_BULLET)] != SIMBE_BULLET:
                    curr_bullet_depth = 1
                elif frame[line_no][0:len(SIMBE_BULLET) + 1] == 1*"\t" + SIMBE_BULLET:
                    curr_bullet_depth = 2
                elif frame[line_no][0:len(SIMBE_BULLET) + 2] == 2*"\t" + SIMBE_BULLET:
                    curr_bullet_depth = 3
                elif frame[line_no][0:len(SIMBE_BULLET) + 3] == 3*"\t" + SIMBE_BULLET:
                    curr_bullet_depth = 4
                elif frame[line_no][0:len(SIMBE_BULLET) + 4] == 1*"    " + SIMBE_BULLET:
                    curr_bullet_depth = 2
                elif frame[line_no][0:len(SIMBE_BULLET) + 8] == 2*"    " + SIMBE_BULLET:
                    curr_bullet_depth = 3
                elif frame[line_no][0:len(SIMBE_BULLET) + 12] == 3*"    " + SIMBE_BULLET:
                    curr_bullet_depth = 4
                else:
                    curr_bullet_depth = 0
    
                if curr_bullet_depth > bullet_depth:
                    new_frame.append("\t"*bullet_depth + "\\begin{itemize}")
                    bullet_depth += 1
                elif curr_bullet_depth < bullet_depth:
                    while (curr_bullet_depth < bullet_depth):
                        bullet_depth -= 1
                        new_frame.append("\t"*bullet_depth + "\\end{itemize}")
    
                if curr_bullet_depth == 0:
                    new_frame.append(frame[line_no])
                else:
                    new_frame.append("\t" + frame[line_no].replace(SIMBE_BULLET, "\\item ", 1))
        frames[frame_no] = new_frame


def write_output(frames, outputfile):
    """ Print out the final product."""
    F = open(outputfile, "w")
    for frame_no in frames:
        frame = frames[frame_no]
        for line in frame:
            F.write(line + "\r")
        F.write("\n% ------------------------------------------------------------------------------------------------------------\n")
    F.write("\\end{document}\n")
    F.close()


def print_frames(frames, start_frame=1):
    """ Print out frames and line numbers."""
    for frame_no in sorted(frames.keys())[start_frame:]:
        print("--------------------------------------")
        for line_no in range(len(frames[frame_no])):
            print(line_no, frames[frame_no][line_no])
    print("--------------------------------------")


# ------------------------------------------------------------------------------------------------------------


# Read file.
inputfile = read_parms()
frames = read_file(inputfile)
#print_frames(frames)
add_frames(frames)

# Deal with ----- (5)
add_lstinputlisting_env(frames, start_frame=1)

# Deal with ----  (4)
add_lstlisting_env(frames)

# Deal with ---   (3)
add_figure_env(frames)

# Deal with --    (2)
add_equation_env(frames)

# Deal with -     (1)
add_itemize_env(frames)

# Write output
outputfile = inputfile.replace(".simbe.tex", ".tex")
write_output(frames, outputfile)



