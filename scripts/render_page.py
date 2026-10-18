import sys,pymupdf
with pymupdf.open(sys.argv[1]) as d:
 d[int(sys.argv[2])-1].get_pixmap(matrix=pymupdf.Matrix(float(sys.argv[4]),float(sys.argv[4]))).save(sys.argv[3])
