

### Python Note:

#### 1. Environmental Variable

|Content |Code|Example|
|-------|---- |-------|
| Create an environmental variable|```$env:environmental_name=environmental_value```| $env:clinet_id='asdfasf123'|
| Call up the specific environmental variables|```Get-ChildItem env:env_name,env:env_name```|Get-ChildItem env:cleint_id|
|Remove the variables|```Step 1) After writing up to "Remove-Item env:", double taps and choose the variable you want to delete.  Step 2) Check if your code follows the next template,Remove-Item Env:\env_name.``` | Remove-Item Env:\client_id,Env:\client_secrets|


