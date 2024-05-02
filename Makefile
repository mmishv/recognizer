up:
	docker-compose -f docker/docker-compose.yml up

up-build:
	docker-compose -f docker/docker-compose.yml up --build

down:
	docker-compose -f docker/docker-compose.yml down

down-remove-volumes:
	docker-compose -f docker/docker-compose.yml down -v

postman-tests:
	docker run --rm --network host -v $$PWD/src/tests/e2e:/etc/newman -t postman/newman:alpine run postman_tests.json \
		--environment environment_local.json \
		--working-dir files/

down-remove-volumes:
	docker-compose -f docker/docker-compose.yml down -v

chmod-versions:
	sudo chmod -R a+w src/migrations/versions/

create-migrations:
	docker-compose -f docker/docker-compose.yml run auto-driver-management alembic revision --autogenerate -m "$(m)"

migrations-upgrade:
	docker-compose -f docker/docker-compose.yml run auto-driver-management alembic upgrade head

migrations-downgrade:
	docker-compose -f docker/docker-compose.yml run auto-driver-management alembic downgrade -1
