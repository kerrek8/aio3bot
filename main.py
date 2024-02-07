import loader
import uvicorn

if __name__ == '__main__':
    uvicorn.run(
        loader.app,
        host='localhost',
        port=80,
    )
