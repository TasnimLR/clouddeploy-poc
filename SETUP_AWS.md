# Guide de mise en place — CI/CD CloudPilot AI sur AWS
**Durée estimée : 45 à 60 minutes**

---

## Ce qu'on va créer

```
GitHub (ton repo) → AWS CodePipeline → AWS CodeBuild → Elastic Beanstalk
```

A chaque `git push`, le pipeline se déclenche automatiquement, lance les tests, et déploie l'API si tout passe.

---

## Étape 0 — Préparer le repo GitHub

1. Crée un nouveau repo GitHub (ex: `cloudpilot-poc`)
2. Copie tous les fichiers du dossier `poc_cloudpilot/` dans ce repo :
   - `app.py`
   - `test_app.py`
   - `requirements.txt`
   - `buildspec.yml`
   - `Procfile`
   - `.ebextensions/python.config`
3. Pousse sur GitHub :
   ```bash
   git init
   git add .
   git commit -m "feat: initial CloudPilot AI PoC"
   git branch -M main
   git remote add origin https://github.com/TON_USERNAME/cloudpilot-poc.git
   git push -u origin main
   ```

---

## Étape 1 — Créer l'environnement Elastic Beanstalk

> AWS Console → **Elastic Beanstalk** → Create Application

**Configuration :**
- Application name : `cloudpilot-ai`
- Platform : `Python`
- Platform branch : `Python 3.11`
- Application code : `Sample application` (on remplacera avec le pipeline)

**Paramètres d'instance :**
- Instance type : `t2.micro` (free tier)
- Key pair : en créer une ou en sélectionner une existante

Cliquer **Create environment** et attendre ~5 minutes que l'environnement soit `Ready`.

> Note l'URL de l'environnement (ex: `http://cloudpilot-ai-env.elasticbeanstalk.com`) — c'est l'URL de ta démo.

---

## Étape 2 — Créer le rôle IAM pour CodeBuild

> AWS Console → **IAM** → Roles → Create role

- Trusted entity : `AWS service` → `CodeBuild`
- Attach policies :
  - `AWSCodeBuildAdminAccess`
  - `AmazonS3FullAccess`
  - `AdministratorAccess-AWSElasticBeanstalk`
- Role name : `CodeBuildCloudPilotRole`

---

## Étape 3 — Créer le projet CodeBuild

> AWS Console → **CodeBuild** → Create build project

**Source :**
- Source provider : `GitHub`
- Repository : ton repo `cloudpilot-poc`
- Branch : `main`

**Environment :**
- Managed image
- OS : `Amazon Linux 2`
- Runtime : `Standard`
- Image : `aws/codebuild/standard:7.0`
- Service role : `CodeBuildCloudPilotRole`

**Buildspec :**
- Use a buildspec file (il lira automatiquement `buildspec.yml` dans ton repo)

**Artifacts :**
- Type : `Amazon S3`
- Bucket : crée un bucket S3 (ex: `cloudpilot-artifacts-TONNOM`)
- Name : `build-output.zip`
- Packaging : `ZIP`

Cliquer **Create build project**.

---

## Étape 4 — Créer le Pipeline CodePipeline

> AWS Console → **CodePipeline** → Create pipeline

### Étape 4.1 — Pipeline settings
- Pipeline name : `cloudpilot-pipeline`
- Service role : créer un nouveau rôle (automatique)
- Artifact store : S3 bucket créé à l'étape 3

### Étape 4.2 — Source stage
- Source provider : `GitHub (Version 2)`
- Cliquer **Connect to GitHub** → autoriser AWS
- Repository : `cloudpilot-poc`
- Branch : `main`
- Detection : `GitHub webhooks` (déclenchement automatique)

### Étape 4.3 — Build stage
- Build provider : `AWS CodeBuild`
- Region : ta région
- Project name : le projet créé à l'étape 3

### Étape 4.4 — Deploy stage
- Deploy provider : `AWS Elastic Beanstalk`
- Application name : `cloudpilot-ai`
- Environment name : l'environnement créé à l'étape 1

Cliquer **Create pipeline** → le premier déploiement démarre automatiquement.

---

## Étape 5 — Vérifier que tout fonctionne

1. Aller sur **CodePipeline** → `cloudpilot-pipeline`
2. Attendre que les 3 étapes (Source, Build, Deploy) soient vertes
3. Aller sur l'URL Elastic Beanstalk et tester :
   ```
   GET http://cloudpilot-ai-env.elasticbeanstalk.com/
   GET http://cloudpilot-ai-env.elasticbeanstalk.com/health
   GET http://cloudpilot-ai-env.elasticbeanstalk.com/pipelines
   ```

---

## Étape 6 — Tester le déclenchement automatique (la démo)

C'est ce que tu montreras pendant la présentation :

1. Modifier `app.py` — par exemple changer la version dans `APP_VERSION = "1.0.1"`
2. Commit et push :
   ```bash
   git add app.py
   git commit -m "feat: upgrade to v1.0.1"
   git push
   ```
3. Aller sur CodePipeline → regarder le pipeline se déclencher en live
4. En ~2-3 minutes, la nouvelle version est déployée

---

## Si un test échoue (pour montrer le comportement)

Modifie temporairement un test pour le faire échouer :
```python
# Dans test_app.py, changer :
assert data["status"] == "healthy"
# en :
assert data["status"] == "broken"  # va faire échouer le pipeline
```

Push → le pipeline s'arrête à l'étape Build → la prod n'est pas touchée. C'est exactement le comportement qu'on veut montrer aux sponsors.

---

## Structure des fichiers

```
cloudpilot-poc/
├── app.py                    # L'API Flask
├── test_app.py               # Tests unitaires (pytest)
├── requirements.txt          # Dépendances Python
├── buildspec.yml             # Instructions pour CodeBuild
├── Procfile                  # Point d'entrée pour Elastic Beanstalk
└── .ebextensions/
    └── python.config         # Config EB
```

---

## En cas de problème

**Le pipeline échoue à l'étape Build :**
- Vérifier les logs CodeBuild (cliquer sur "Details" à côté du stage rouge)
- Souvent : problème de permissions IAM → ajouter `AdministratorAccess` au rôle temporairement

**Elastic Beanstalk reste en "Updating" longtemps :**
- Normal, ça peut prendre 3-5 minutes
- Vérifier les logs EB : EB Console → votre env → Logs → Request Logs

**GitHub ne se connecte pas à CodePipeline :**
- Utiliser **GitHub (Version 2)** et pas Version 1
- Dans le Learner Lab, autoriser GitHub via OAuth

---

*Setup guide — CloudPilot AI PoC | AWS Academy 2026*
