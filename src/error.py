
NO_CONFIG_FILE = "Config file '{config_file_path}' not found "

INVALID_DIMENSIONS = "Invalid dimensions format in the configuration file"
NO_EMPTY_LINE = "Expected an empty line after dimensions in the configuration file"
INVALID_LINE_COUNT = "Expected {expectedLineCount} lines according to given dimensions in the configuration file, got {trueLineCount}" 
INVALID_LAYER_HEADER = "Invalid layer header format and/or layer index at line {lineNumber}, expected 'Layer {layerIndex}:'"
INVALID_ROW_FORMAT = "Invalid row format at layer {layerIndex}, row {rowIndex}"

INVALID_SPHINX_LAYER = "Invalid sphinxes: sphinx found on layer {layerIndex}, onlyallowed on layer 0"
INVALID_SPHINX_COUNT = "Invalid sphinxes: expected exactly 1 sphinx per player"

INVALID_PHARAOH_LAYER = "Invalid pharaohs: pharaoh found on layer {layerIndex}, only allowed on layer K-1"
INVALID_PHARAOH_COUNT = "Invalid pharaohs: expected exactly 1 pharaoh per player"


INVALID_PATTERN = "Move does not conform to expected pattern"
OUT_OF_BOUNDS_SRC = "The move {encodedMove} source is out of bounds"
OUT_OF_BOUNDS_DST ="The move {encodedMove} destination is out of bounds"

EMPTY_CELL = "The cell {cell} is empty"
OWNERSHIP_ERROR = "Player {x} does not control piece {cell}"
ILLEGAL_MOVEMENT = "Piece {piece} cannot be moved"

NOT_ADJACENT=  "Piece at {cell1} cannot be moved to {cell2}, not adjacent"
DST_OCCUPIED = "Piece at {cell1} cannot be moved to {cell2}, destination is already occupied"

INVALID_SCARAB_SWAP = "Piece at {cell1} cannot be moved to {cell2}, invalid scarab swap"
INVALID_PHARAOH_MOVE = "Pharaoh cannot be moved to lower layer"