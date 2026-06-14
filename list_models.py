from lmstudio_client import create_client

def main():
    client = create_client()
    models = client.models.list()

    print("Models:")
    for models in models.data:
        print(" - ", models.id)

if __name__ == "__main__":
    main()