<!DOCTYPE html>
<html lang="fr">
	<head>
		<meta charset="utf-8" />
		<link rel="stylesheet" href="/static/css/admin.css" />
		<title>Suivi</title>
	</head>

	<body>
        <header>
            <nav id="navbar">
                <ul>
                    <li><a href="/">Application</a> </li>
                    <li><a href="/admin">Utilisateurs</a> </li>
                </ul>
            </nav>
            <p>{{user}} <a href="/logout">| logout</a></p>
        </header>

        <section id="content">
            {{!base}}
        </section>

	</body>
</html>
