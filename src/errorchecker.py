
# from outstream import OutStream 
# from instream import InStream
# from error import *


# class ErrorChecker:
#     def __init__(self,filename):
#         self.m = Manager(filename)
    
#     def check_dimensions(self,line1):
#         tokens = line1.strip().split(',')
#         if len(tokens) != 3:
#             return False
#         else:
#             self.m.set_n = int(tokens[0])
#             self.m.set_m = int(tokens[1])
#             self.m.set_k = int(tokens[2])
#             return True

#     def check_empty_line(self, line2):
#         if line2 != "":
#             return False
        
#     def check_num_lines(self,count,expected_lines): 
#         if expected_lines != count:
#             self.write_error_to_outfile(self._file, INVALID_LINE_COUNT.format(expectedLineCount=expected_lines,trueLineCount=count))
       
#     def check_layers(self):
#         track = 0
#         for layer_index in range(self._k):
#             if self._lines[track] != f"Layer {layer_index}:":
#                 self.write_error_to_outfile(self._file,INVALID_LAYER_HEADER.format(lineNumber = track, layerIndex = layer_index)) 
#                 #add other info
#                 #exit
#             track+=1
            
#             for row_index in range(self._m):
#                 row = (self._lines[track])
#                 tokens = row.strip().split(' ')
               
#                 if len(tokens) != self._n:
#                     self.write_error_to_outfile(self._file,INVALID_ROW_FORMAT.format(layerIndex = layer_index,rowIndex = row_index))
                 
#                 else: 
#                     for cell in range(self._n):
#                         s = tokens[cell]
#                         if s[0] != "(" or s[len(s)-1] != ")" or s[2] != ",": #also check if charaters are valid
#                             self.write_error_to_outfile(self._file,INVALID_ROW_FORMAT.format(layerIndex = layer_index,rowIndex = row_index))
#                 track +=1
#             track +=1
         
        
        