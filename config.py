import pygame

pygame.font.init()

def text_speech(sc, pos, text, font, color=(255,255,255)):
	rendered_text = font.render(text, True, color)
	sc.blit(rendered_text, rendered_text.get_rect(center=pos))
	
class sc:
	cell_size = 78
	border_size = 2
	cells_num = 4
	animate_time = cells_num/10
	animate_xy = cell_size*cells_num + border_size*(cells_num-1)

	w = cell_size*cells_num + border_size*(cells_num+1)
	h = cell_size*cells_num + border_size*(cells_num+1) + 50

	fonts = []
	for i in range(8,4,-1):
		fonts.append(pygame.font.Font(None, int(cell_size*i/10)))

	BG_COLOR = (120, 110, 100)
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

	SURFACES = {}
	SURFACES[0] = pygame.Surface((cell_size, cell_size))
	SURFACES[0].fill((30,30,30))
	text_speech(SURFACES[0], (cell_size//2,cell_size//2), '?', fonts[0], (240,240,240))
	for i in range(1,len(CELL_COLOR)-3):
		val = 2**i
		SURFACES[val] = pygame.Surface((cell_size, cell_size))
		SURFACES[val].fill(CELL_COLOR[val])
		text_speech(SURFACES[val], (cell_size//2,cell_size//2), str(val), fonts[min(len(str(val))-1,len(fonts))], TEXT_COLOR[val])