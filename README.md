# Simbe

Simbe is a ultralight markup language developed for quickly creating and modifying slides heavy in mathematical notation and programming language code. I created it first in 2013 when I had to prepare 600+ slides for teaching a new course. For slides containing math, PowerPoint and Keynote are not feasible options, and this is where LaTeX Beamer shines. However, LaTeX can be heavy in markup overhead, especially when writing bulleted lists. Another realization was that for most slides, there are really only a handful of things I'd like to be able to do: add bullets, indent bullets, add mathematical notation, add syntax highlighted code, and add figures. These cover about 99% of what I'd like to have on my teaching slides.

Simbe is a very simple LaTeX preprocessor. The name is short for Simple LaTeX Beamer, and it's written in Python 3. The script converts a Simbe text file (`slides.simbe.tex`) to a standard LaTeX Beamer file (`slides.tex`). The latter then needs to be compiled using LaTeX to generate PDF slides. If Simbe (`simbe.py`) and the source slides (`slides.simbe.tex`) are in the same directory, then all you need is type the following in a terminal: `python simbe.py slides.simbe.tex`. The output file `slides.tex` will be saved in the same directory.

The syntax and functionality of Simbe are by design extremely simple. Operators start in the leftmost position in the source file; the only exception is nested bullets, which are created by hitting tab (once or more) and then inserting the bullet operator. With the exception of slide creation, all operators consist of two or more dashes. As a useful mnemonic, the number of dashes corresponds to the number of characters in eq (show equation in display mode), fig (show figure), code (show syntax highlighted typed code), codes (show syntax highlighted code inserted from a file). If you don't want numbered equations, you can use the `nn` (no number) option below. Inline equations are created with the usual $p=mv$ LaTeX syntax.

Syntax for Simbe:
- Create a new slide and title
  ```
  **History of Science
  ```
- Insert bullet and indented bullet
  ```
  -There are a few famous equations in science.
    -Some are more famous than others.
   ```
- Insert numbered equation
  ```
  --E=mc^2--
  ```
  ```
  --
  E=mc^2
  --
  ```
- Insert non-numbered equation
  ```
  --E=mc^2--nn
  ```
  ```
  --
  E=mc^2
  --nn
  ```
- Insert figure; specify relative width; add caption (optional)
  ```
  ---
  my_figure.pdf, 0.4
  -This is the caption.
  ---
  ```



- \verb+---+

- Start and end code segment (code) <br />
- 
- \verb+----+
- Insert code segment from file (codes) <br />
- 
- 
- : \verb+-----filename.py-----+









