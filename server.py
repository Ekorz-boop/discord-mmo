from app import app, create_tables

def main():
    create_tables()
    app.run()

if __name__ == '__main__':
    main()