1.
az login

2.
az group create --name qianResourceGroup --location westus

3.
az acr create --resource-group qianResourceGroup --name qiancontainerregistry --sku Basic

4.
az acr login --name qiancontainerregistry

5. 
docker tag 95b0800a7926 qiancontainerregistry.azurecr.io/proxyweb:v3

6.
docker push qiancontainerregistry.azurecr.io/proxyweb:v3

7.
az acr repository list --name qiancontainerregistry --output table

8.
DNS_NAME_LABEL="qian-proxy-test"


9.
RES_GROUP=qianResourceGroup # Resource Group name
ACR_NAME=qiancontainerregistry       # Azure Container Registry registry name
AKV_NAME=qiankeyvault       # Azure Key Vault vault name

SERVICE_PRINCIPAL_NAME=qianacrsp

RESOURCE_GROUP_ID=$(az group show --name $RES_GROUP --query "id" --output tsv)

PASSWORD=$(az ad sp create-for-rbac --name $SERVICE_PRINCIPAL_NAME --scopes $RESOURCE_GROUP_ID --role AcrPush --query "password" --output tsv)
USER_NAME=$(az ad sp list --display-name $SERVICE_PRINCIPAL_NAME --query "[].appId" --output tsv)

echo "Service principal ID: $USER_NAME"
echo "Service principal password: $PASSWORD"



10. 
DNS_LABEL_NAME="qian-proxy-test"
REGION="westus"
az container create --resource-group qianResourceGroup \
--name proxyweb \
--image qiancontainerregistry.azurecr.io/proxyweb:v3 \
--ports 80  \
--dns-name-label $DNS_LABEL_NAME \
--location westus \
--registry-username $USER_NAME \
--registry-password $PASSWORD 

URL="${DNS_LABEL_NAME}.${REGION}.azurecontainer.io"
echo $URL

#### get logs ###
az container logs --resource-group $RES_GROUP --name proxyweb --container-name proxyweb 


az container delete --resource-group $RES_GROUP --name proxyweb 

az container list --resource-group $RES_GROUP

