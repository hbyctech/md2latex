import argparse
import os 
import sys




def main():
    # Parse arguments
    parser = argparse.ArgumentParser(description='Convert markdown to latex')
    parser.add_argument('input', type=str, help='Input file')
    parser.add_argument('-o', '--output', type=str, help='Output file')
    # type: article, report, book; default: article
    parser.add_argument('-t', '--type', type=str, help='Type of document: article, report, book')
    args = parser.parse_args()
    
    # # if -h is passed print help
    # if args.help:
    #     parser.print_help()
    #     sys.exit(0)
        
    # get type, if not defined, set to article
    if args.type:
        type = args.type
    else:
        type = 'article'
        
    # check if input file exists
    if not os.path.isfile(args.input):
        print('Input file does not exist')
        sys.exit(1)
        
    # read input file into memory
    with open(args.input, 'r') as f:
        lines = f.readlines()
        
    # strip lines and remove empty lines
    lines = [line.strip() for line in lines]
    # remove the empty lines at the beginning only
    while lines[0] == '':
        lines = lines[1:]
    
    # find the biggest heading
    biggest_heading = 0
    for line in lines:
        if line.startswith('#'):
            heading = len(line.split(' ')[0])
            if (heading < biggest_heading) | (biggest_heading == 0):
                biggest_heading = heading
    # 0 -- no headings
    # 1 -- # is the biggest heading
    # 2 -- ## is the biggest heading
    # ...
    
    title = ''
    author = ''
    date = '\\today'
    
    # count how many biggest headings there are
    biggest_heading_count = 0
    if biggest_heading == 0:
        biggest_heading_count = 0
    else:
        for line in lines:
            if line.startswith('#' * biggest_heading):
                # also make sure ### don't count in ## list
                if len(line.split(' ')[0]) == biggest_heading:
                    biggest_heading_count += 1
    if (biggest_heading_count == 1):
        # the biggest heading is the beggining of the document
        if lines[0].startswith('#' * biggest_heading):
            title = lines[0].replace('#' * biggest_heading, '').strip()
            # remove the first line from lines
            lines = lines[1:]

    # convert lines to latex
    latex_lines = []    
    # add document type
    latex_lines.append('\\documentclass{' + type + '}\n')
    # add packages
    latex_lines.append('\\usepackage{amsmath}\n')
    latex_lines.append('\\usepackage{amssymb}\n')
    latex_lines.append('\\usepackage{graphicx}\n')
    latex_lines.append('\\usepackage{hyperref}\n')
    latex_lines.append('\\usepackage{float}\n')
    latex_lines.append('\\usepackage{listings}\n')
    latex_lines.append('\\usepackage{color}\n')
    latex_lines.append('\\usepackage{enumitem}\n')
    latex_lines.append('\\usepackage{titling}\n')
    
    # add title, author, date
    latex_lines.append('\\title{' + title + '}\n')
    latex_lines.append('\\author{' + author + '}\n')
    latex_lines.append('\\date{' + date + '}\n')
    
    # add an empty line
    latex_lines.append('\n')
    
    # begin the document context
    latex_lines.append('\\begin{document}\n')
    
    # make title
    latex_lines.append('\\maketitle\n')
    
    # add context
    for line in lines:
        # if line starts with #, it is a heading
        if line.startswith('#'):
            heading = len(line.split(' ')[0])
            heading_order = heading - biggest_heading - 1
            # remove the heading from the line
            line = line.replace('#' * heading, '').strip()
            # add the heading to the latex line
            latex_lines.append('\\' + 'sub' * (heading_order - 1) + 'section{' + line + '}\n')
        else:
            latex_lines.append(line + '\n')
    
    # end the document context
    latex_lines.append('\\end{document}\n')
    
    # write output file
    if args.output:
        with open(args.output, 'w') as f:
            f.writelines(latex_lines)
    else:
        with open(args.input.split('.')[0] + '.tex', 'w') as f:
            f.writelines(latex_lines)
        
# main function
main()
     