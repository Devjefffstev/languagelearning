#!bin/bash
nameDeploy=rollout-deploy-example
rolloutFile=k8s_rollout_example.yaml
## create a deployment 
clear
rm -r $rolloutFile
kubectl delete deploy $nameDeploy 
kubectl delete -f $rolloutFile 

echo ""
echo "Creating deployment with first revision -----------------------------------------------------------------------------------------------------------\n"
#kubectl create deploy rollout-example-deployment --image=nginx --image=busybox:latest --image=ubuntu:latest --replicas=2 
# if you use this command you canot see the changes on your rollout history
#kubectl create deploy $nameDeploy --image=nginx --replicas=8 --dry-run=client -o yaml | kubectl apply -f - --record
kubectl create deploy $nameDeploy --image=nginx --replicas=10 --dry-run=client -o yaml > $rolloutFile
kubectl create -f $rolloutFile --record 
echo ""
echo -e "Check deploy ----------------------------------------------------------------------------------------------------\n"
echo ""
kubectl get deploy -o wide 
echo ""
echo -e "Describe deployment ---------------------------------------------------------------------------------------------------------------------\n"
kubectl describe deploy $nameDeploy
echo ""
echo "Rollout history  ---------------------------------------------------------------------------------------------------------------------\n"
kubectl rollout history deploy $nameDeploy
echo ""
echo "Rollout status   ---------------------------------------------------------------------------------------------------------------------\n"
kubectl rollout status deploy $nameDeploy
echo ""
echo -e "Pods of the deployment ---------------------------------------------------------------------------------------------------------------------\n"
kubectl get pods --selector=app=$nameDeploy -o wide 
echo ""
## Witing for rollback
waitfunction() {
	waittime=$1
	for ((i=1; i<=waittime; i++)); do
	    echo "Waiting $waittime-$i"
	    sleep 1
	done
}
waitfunction 5
echo ""
echo -e "Starting rolling out deployment ---------------------------------------------------------------------------------------------------------------------\n"
kubectl set image deploy $nameDeploy nginx=nginx:1.12 --record
echo ""
echo -e "Starting rolling out deployment ---------------------------------------------------------------------------------------------------------------------\n"
kubectl rollout status deploy $nameDeploy
echo ""
echo -e "Describe deployment ---------------------------------------------------------------------------------------------------------------------\n"
kubectl describe deploy $nameDeploy
echo ""
echo "Rollout history  ---------------------------------------------------------------------------------------------------------------------\n"
kubectl rollout history deploy $nameDeploy
echo ""
echo -e "Pods of the deployment ---------------------------------------------------------------------------------------------------------------------\n"
kubectl get pods --selector=app=$nameDeploy -o wide 
echo ""
waitfunction 5
echo -e "Creatining version deployment ---------------------------------------------------------------------------------------------------------------------\n"
kubectl set image deploy $nameDeploy nginx=nginx:1.12-perl --record
kubectl set image deploy $nameDeploy nginx=nginx:1.13.9 --record
kubectl set image deploy $nameDeploy nginx=nginx:1.13 --record
echo ""
echo "Rollout history  ---------------------------------------------------------------------------------------------------------------------\n"
kubectl rollout history deploy $nameDeploy
echo ""
echo "Rollout undo to a revision"
kubectl rollout undo deploy $nameDeploy --to-revision=3 

echo ""
echo -e "Describe deployment ---------------------------------------------------------------------------------------------------------------------\n"
kubectl describe deploy $nameDeploy
rm -r $rolloutFile
