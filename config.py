import pygame

class sc:
	cell_size = 75
	border_size = 5
	cells_num = 4
	animate_time = cells_num/10

	w = cell_size*cells_num + border_size*(cells_num+1)
	h = cell_size*cells_num + border_size*(cells_num+1) + 50

	BG_COLOR = (158, 148, 138)
	CELL_COLOR = {
		0:   (187, 173, 160), 2:    (238, 228, 218), 4:    (217, 204, 180),
		8:   (242, 177, 121), 16:   (245, 149,  99), 32:   (246, 124,  95),
		64:  (246,  94,  59), 128:  (237, 207, 114), 256:  (237, 204,  97),
		512: (237, 200,  80), 1024: (237, 197,  63), 2048: (237, 194,  46),
		
		4096: (238, 228, 218),
		8192: (237, 194, 46),
		16384: (242, 177, 121),
		32768: (245, 149, 99),
		65536: (246, 124, 95)}

	TEXT_COLOR = {
		0: (187, 173, 160), 2: (119, 110, 101), 4: (119, 110, 101),
		8: (249, 246, 242), 16: (249, 246, 242), 32: (249, 246, 242),
		64: (249, 246, 242), 128: (249, 246, 242), 256: (249, 246, 242),
		512: (249, 246, 242), 1024: (249, 246, 242), 2048: (249, 246, 242),

		4096: (119, 110, 101),
		8192: (249, 246, 242),
		16384: (119, 110, 101),
		32768: (119, 110, 101),
		65536: (249, 246, 242)}