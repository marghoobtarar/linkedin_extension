# linkedin_extension
## backend
python3.8
```
virtualenv env
source env/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

```
## fron-end
```
cd frontend
npm install && npm run

```
## google extension
```
 npm run build

```
unpack the dist folder in the google extension and run it.


## password error modification

update the rest_framework_simplejwt.views.py file in environment(env) folder where all the python packages has been installed (line #23 post method)
```
    def post(self, request, *args, **kwargs):
        key_lookup = 'email'
        if key_lookup in request.data:
            try:
                User.objects.get(email = request.data['email'])
            except:
                return Response({"detail":" The email you entered doesn't belong to an account. Please check your login information and try again."}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                serializer = self.get_serializer(data=request.data)

                try:
                    serializer.is_valid(raise_exception=True)
                except TokenError as e:
                    raise InvalidToken(e.args[0])

                return Response(serializer.validated_data, status=status.HTTP_200_OK)
        else:
            serializer = self.get_serializer(data=request.data)

            try:
                serializer.is_valid(raise_exception=True)
            except TokenError as e:
                raise InvalidToken(e.args[0])

            return Response(serializer.validated_data, status=status.HTTP_200_OK)


```
