@echo off

REM Stop and remove the container
docker stop pm-mvp-container
docker rm pm-mvp-container

echo Container stopped and removed.
