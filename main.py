import loader
import uvicorn

if __name__ == '__main__':
    uvicorn.run(
        loader.app,
        host='0.0.0.0',
        port=80,
    )
