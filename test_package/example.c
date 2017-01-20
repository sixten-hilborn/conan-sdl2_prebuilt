#include <stdio.h>
#include <SDL2/SDL.h>
#include <SDL2/SDL_image.h>
#include <SDL2/SDL_mixer.h>
#include <SDL2/SDL_ttf.h>

int main(int argc, char *argv[]) {
	if (SDL_Init(SDL_INIT_VIDEO) != 0) {
		printf("SDL_Init Error: %s\n", SDL_GetError());
		return 1;
	}
	if (TTF_Init() != 0) {
		printf("TTF_Init Error: %s\n", TTF_GetError());
		return 1;
	}
	// Just make sure we can link to SDL_image
	IMG_Load("");

	return 0;
}