# NVI Solutions test task

![preview](https://github.com/romaokorosso/nvi_solutions_test_task/blob/main/img.png?raw=true)

## Task checklist

[+] make easy web application

[+] upload images

[+] recognize image object

[+] return result and image size

## Built With

* [Python3.10](https://www.python.org/downloads/release/python-3100/)
* [FastAPI](https://fastapi.tiangolo.com/)
* [PyTorch](https://pytorch.org/)
* [Docker](https://www.docker.com/)
* [Docker-compose](https://docs.docker.com/compose/)

## Getting Started

1. Install docker and docker-compose using links above (skip if already installed)
2. Clone this repo `git clone https://github.com/romaokorosso/nvi_solutions_test_task.git`
3. Go to project directory `cd nvi_solutions_test_task`
4. ```bash
    cp .env.example .env
   ```
5. Run `docker-compose up -d --build` in project directory (m.b need to use `sudo`)
6. Open `http://{APP_HOST}:{APP_PORT}/` in your browser
7. Upload image and click "Submit Query" button
8. Wait for result
9. Enjoy!

