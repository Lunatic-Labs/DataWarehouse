# DataWarehouse
## Setup 
### Python Dependencies 
Please install your python packages in a virtual environemnt. This will protect our development from meddling with other projects. Especially useful if you are developing for other classes or something. To do this, investigate this link: https://docs.python.org/3/tutorial/venv.html
run `pip install .` in the main directory
### Postgresql
You will need to install and run a local postgresql server in order to develop on your own machine. 
### Environment Variables
You will need to export these environment variables in order for the application to run correctly. You can do this by including a `.env` file in the root directory of the project, or by manualy exporting them, or by writing an `.sh` file to export them for you on startup. 
To manually export them, run this command in your environment
`export <env var key>=<env var value>`
for example:
`export FLASK_ENV='develop'` 
#### Required
* `DATABASE_URL` - either your local or the online database url. Example: `DATABASE_URL='postgresql://postgres:postgres@localhost:5432/data_warehouse'`
* `FLASK_APP` - The app name. Set this to `datawarehouse`
#### Suggested
* `FLASK_DEBUG` - This tells flask to either run the app in production mode or developer mode. You probably want developer mode. Either `0` for off, or `1` for on.


## Running the app
after completing the setup process, use command `flask run` in the console to run. 