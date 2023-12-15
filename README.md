# Template for ECS639U Group Coursework

This template should be used as the starting point for your group coursework in the module ECS639U Web Programming (at Queen Mary University of London). Use Git (github.qmul.ac.uk) to collaborate on the coursework with your group members. Module leader: Paulo Oliva <[p.oliva@qmul.ac.uk](mailto:p.oliva@qmul.ac.uk)>

## Important 

The database is excluded from this Git repository. To see the populated project, complete with test users, articles, and comments, please visit the deployment URL. If you want to build the project on your machine, you can follow the provided instructions under `Local development`.

## Deployment URL (Openshift)

https://group33-web-apps-ec21385.apps.a.comp-teach.qmul.ac.uk/

## Users

| Username | Password       | Superuser |
|----------|----------------|-----------|
| admin    | admin          | Yes       |
| Beetle   | Beetlejuice123 | No        |
| Fidel    | Castro123      | No        |
| Donald   | Trump2024      | No        |
| Joe      | JoeBiden1331   | No        |
| Jesus    | ChristIsKing1  | No        |

## Contribution

| Student ID | Name  | Assigned Task                                           | Final Deliverable                                |
|------------|-------|--------------------------------------------------------|---------------------------------------------------|
| 210343496     | Tajul | Backend                                                | Worked on APIs and deployment                    |
| 210292264     | Lukas | Frontend                                               | Worked on frontend and connected to backend     |
| 200495787     | Getuard  | Frontend styling and testing                           | Designed website                                 |
| 200433262     | Mohammed  | Login and register page, modeling of data   | Login and register page, modeling of data        |







## Local development

To run this project in your development machine, follow these steps:

1. Create and activate a conda environment

2. Fork this repo and clone your fork (or clone the forked repo of one of your team members), e.g.

    ```console
    $ git clone https://github.qmul.ac.uk/<username>/cwgroup
    ```

3. Install Python dependencies (main folder):

    ```console
    $ pip install -r requirements.txt
    ```

4. Collect static files

    ```console
    $ python manage.py collectstatic
    ```

5. Create a development database:

    ```console
    $ python manage.py migrate
    ```

6. Install JavaScript dependencies (from 'frontend' folder):

    ```console
    $ npm install
    ```

7. If everything is alright, you should be able to start the Django development server from the main folder:

    ```console
    $ python manage.py runserver
    ```

8. and the Vue server from the 'frontend' sub-folder:

    ```console
    $ npm run dev
    ```

8. Open your browser and go to http://localhost:5173, you will be greeted with a template page.

## OpenShift deployment

Once your project is ready to be deployed you will need to 'build' the Vue app and place it in Django's static folder.

1. The build command in package.json and the vite.config.ts files have already been modified so that when running 'npm run build' the generated JavaScript and CSS files will be placed in the mainapp static folder, and the index.html file will be placed in the templates folder:

    ```console
    $ npm run build
    ```

2. You should then follow the instruction on QM+ on how to deploy your app on EECS's OpenShift live server.

## License

This code is dedicated to the public domain to the maximum extent permitted by applicable law, pursuant to [CC0](http://creativecommons.org/publicdomain/zero/1.0/).
