# Deployments Doc

## NOTES:


**This instrcution will allow us to minimize the depepndecies to each other and conflict of deployment and code.**

-  [ Each Developer must create the own branch based on the features ] 
-  [ First Deploy the Created features branch on the test server and verify it ] 
-  [ Once it is done create the merge into kick and deploy and verify ] 


## Test server deployment

1. Open the [`jenkins URL` ](https://jenkins.i69app.com/) [https://jenkins.i69app.com/]
2. Do the authorization through gitlab credential, **_if you have already opened the gitlab session in the browser and would be automatically loggged in._**

![Alt text](Deployment-artifact/ref-1.PNG?raw=true "Reference-1")
![Alt text](Deployment-artifact/ref-2.PNG?raw=true "Reference-2")

3. Click on the Backend deployment Job and Select the build with parameter.

![Alt text](Deployment-artifact/ref-3.PNG?raw=true "Reference-3")

4. Give the branch as input and click on the build.
![Alt text](Deployment-artifact/ref-4.PNG?raw=true "Reference-4")

5. Once the build is running click on the console log [Input requested] `to complete the deployment and rollback - Select the input ROLLBACKSTAGE`.

![Alt text](Deployment-artifact/ref-5.PNG?raw=true "Reference-5")
![Alt text](Deployment-artifact/ref-6.PNG?raw=true "Reference-6")

```
[Input requested] 
- Finish: To Proceed with live deployment - NA now 
- ROLLBACKSTAGE: Rollback to just previous version 
```


