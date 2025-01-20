run-staging:
	docker-compose -f docker-compose-staging.yml --env-file .env.staging up -d --build --force-recreate

stop-staging:
	docker-compose -f docker-compose-staging.yml down -v --remove-orphans
