up:
	docker-compose -f docker-compose.yml up

up-build:
	docker-compose -f docker-compose.yml up --build

down:
	docker-compose -f docker-compose.yml down

down-remove-volumes:
	docker-compose -f docker-compose.yml down -v

down-remove-volumes:
	docker-compose -f docker-compose.yml down -v
