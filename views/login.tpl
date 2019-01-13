<!DOCTYPE html>
<html lang="fr">
	<head>
		<meta charset="utf-8" />
		<link rel="stylesheet" href="/static/css/app.css" />
		<title>Suivi</title>
	</head>

	<body>
        <section id="log">
            <h1>Login</h1>
            <form method="post" action="/login_form">
                <label for="login">Nom d'utilisateur:</label> <br />
                <input id="login" name="login" type="text"/> <br />
                <label for=password>Mot de passe:</label> <br />
                <input id="password" name="password" type="password"/> <br />
                <br />
                <input id="submit" type="submit" value="Envoyer"/>
            </form>
        </section>
        <canvas id="canvas" width="1000" height="600"></canvas>
    </body>
    <script src="/static/js/accueil.js"></script>
</html>
