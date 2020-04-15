
image:

	@docker build -t luisalejandro/fb-last-post-from-feed:latest .

message:

	@docker run -it --rm -u luisalejandro --env-file .env \
		-v $(PWD):/home/luisalejandro/fb-last-post-from-feed \
		-w /home/luisalejandro/fb-last-post-from-feed \
		luisalejandro/fb-last-post-from-feed:latest python entrypoint.py

console:

	@docker run -it --rm -u luisalejandro --env-file .env \
		-v $(PWD):/home/luisalejandro/fb-last-post-from-feed \
		-w /home/luisalejandro/fb-last-post-from-feed \
		luisalejandro/fb-last-post-from-feed:latest bash
