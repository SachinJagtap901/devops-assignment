Project Workflows
 1. Application Development Workflow
     Developer------Codes/Uodates Flask application----Write/update unit tests----Run pytest locally---Git commit---Push to GitHub main branch

2. CI/CD Workflow
                    GitHub
                       │
                       │ Push to main
                       ▼
                  Jenkins Pipeline
                       │
             ┌─────────┴─────────┐
             ▼                   ▼
          Build              Unit Test
             │                   │
             └─────────┬─────────┘
                       │
                    Success
                       │
                       ▼
                 Docker Build
                       │
                       ▼
                Docker Hub Push
                       │
                       ▼
             Kubernetes Deployment
                       │
                       ▼
                Rolling Update
                       │
                       ▼
                 Application
   
   3. Jenkins stages
      Stage 1 — Build
                Jenkins creates a Python virtual environment and installs dependencies
      Stage 2 — Unit Test
                The pipeline continues only when the tests pass.
      stage 3 - Docker Build
                The Jenkins build number is used as the Docker image tag.
      stage 4 - Docker Hub Push
                Jenkins retrieves the Docker Hub credentials from Jenkins Credentials and pushes the image
      stage 5 - Kubernetes Deployment
                Jenkins updates the Kubernetes Deployment

   4. Kubernetes Runtime Workflow
                   Client
                      │
                      ▼
                NGINX Ingress
                      │
                      ▼
             devops-api-service
                      │
              ┌───────┴───────┐
              ▼               ▼
           Pod 1            Pod 2
              │               │
              └───────┬───────┘
                      ▼
                 Flask API
                   :5000
    
    5. Health Check Workflow
       Readiness Probe
             Healthy → Pod receives traffic
             Unhealthy → Pod removed from Service endpoints
       Liveness Probe
             Healthy → Container continues
             Failed repeatedly → Container restarted

   6. Autoscaling Workflow
      Configured HPA as below.
        Minimum replicas: 2
        Maximum replicas: 5
        CPU target:       70%
        Memory target:    80%
                  Application
                        │
                        ▼
                 Resource Usage
                        │
                        ▼
                       HPA
                  ┌─────┴─────┐
                  │           │
              Below target   Above target
                  │           │
                  ▼           ▼
             Maintain      Scale Pods
             replicas      2 → 3 → 4 → 5

   7. Rolling Deployment Workflow

      strategy:
          type: RollingUpdate
          rollingUpdate:
              maxUnavailable: 0
              maxSurge: 1

         Current version
      sachinj6277/devops-api:8
              │
              │ Jenkins deploys
              ▼
      New version
      sachinj6277/devops-api:9
              │
              ▼
      Kubernetes RollingUpdate
              │
         ┌────┴────┐
         ▼         ▼
      Old Pods   New Pod
         │         │
         │      Health check
         │         │
         │      Ready ✓
         │         │
         └─────────┘
              │
              ▼
      Old Pod removed
              │
              ▼
      New version running

 8. Rollback Workflow

       New Deployment
            │
            ▼
      Application problem
            │
            ▼
      kubectl rollout undo
            │
            ▼
      Previous version
            │
            ▼
      Healthy application

9. Complete Project Workflow.

┌──────────────────────┐
│      Developer       │
└──────────┬───────────┘
           │
           │ git push
           ▼
┌──────────────────────┐
│       GitHub         │
│       main           │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│       Jenkins        │
├──────────────────────┤
│ 1. Build             │
│ 2. Unit Test         │
│ 3. Docker Build      │
│ 4. Docker Push       │
│ 5. Kubernetes Deploy │
└──────────┬───────────┘
           │
           │ Docker image
           ▼
┌──────────────────────┐
│      Docker Hub      │
│ devops-api:<tag>     │
└──────────┬───────────┘
           │
           │ image pull
           ▼
┌────────────────────────────────┐
│       Kubernetes Cluster       │
│                                │
│  ┌──────────────────────────┐  │
│  │ Deployment               │  │
│  │ replicas: 2–5            │  │
│  └────────────┬─────────────┘  │
│               │                │
│        ┌──────┴──────┐         │
│        ▼             ▼         │
│      Pod 1         Pod 2       │
│        │             │         │
│        └──────┬──────┘         │
│               │                │
│        Service                │
│               │                │
│        NGINX Ingress           │
│               │                │
└───────────────┼────────────────┘
                │
                ▼
             Client



10. Linear
    Developer → GitHub → Jenkins CI → Unit Testing → Docker Build → Docker Hub → Kubernetes Rolling Deployment → Service → NGINX Ingress → Application, with HPA providing automatic scaling and Kubernetes probes providing health management.
