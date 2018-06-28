import Constellation

@Constellation.MessageCallback()
def SimpleMessageCallback(data):
    "MessageCallback description with one parameter"
    Constellation.WriteInfo('Input  = ' + str(data))

@Constellation.MessageCallback()
def ComplexMessageCallback(data):
    "MessageCallback with object parameter"
    Constellation.WriteInfo(data.A)
    Constellation.WriteInfo(type(data.A))
    Constellation.WriteInfo(type(data.B))
    Constellation.WriteInfo(data.C)

@Constellation.MessageCallback()
def MultipleParameterCallback(a, b, c):
    '''
    This is a MessageCallback with 3 parameters

    The description can be on several lines and you can also describe the parameters like this:

    :param string a: The 'a' parameter is a string !
    :param int b: An integer parameter
    :param bool c: A boolean and optional parameter with a default value [default:true]
    '''
    Constellation.WriteInfo(a)
    Constellation.WriteInfo(b)
    Constellation.WriteInfo(c)

@Constellation.MessageCallback()
def MultipleParameterCallbackWithContext(a, b, c, context):
    '''
    This is a MessageCallback with 3 parameters and a context

    The description can be on several lines and you can also describe the parameters like this:

    :param string a: The 'a' parameter is a string !
    :param int b: An integer and optional parameter [default:10]
    :param bool c: A boolean and optional parameter with a default value [default:true]
    '''
    Constellation.WriteInfo("Sender : %s" % context.Sender.FriendlyName)
    Constellation.WriteInfo(a)
    Constellation.WriteInfo(b)
    Constellation.WriteInfo(c)

@Constellation.MessageCallback("MyMethodWithWhithoutParameter")
def NoParamterWithCustomMessageKey():
    '''
    MessageCallback without parameters and custom key
    This MessageCallback is registered on Constellation as 'MyMethodWithWhithoutParameter'
    '''
    Constellation.WriteInfo(a)
    Constellation.WriteInfo(b)
    Constellation.WriteInfo(c)

@Constellation.MessageCallback(isHidden = True)
def HiddenMessageCallback():
    "Hidden message callback"
    Constellation.WriteInfo("I'm here !!")

@Constellation.MessageCallback()
def MessageCallbackWithReturn(user, password, context):
    '''
    MC with response (this is a Saga)

    :param string user: The username
    :param string password: The password
    :return bool:true if user match
    '''
    Constellation.WriteInfo("Sender : %s" % context.Sender.FriendlyName)
    Constellation.WriteInfo("User=%s Password=%s" % (user, password))
    #Constellation.SendResponse(context, user == password)  # Send response with the static SendResponse method
    #context.SendResponse(user == password)                 # Send response with the SendResponse method on context
    return user == password                                 # Send response for this current context by a simple "return" the value

@Constellation.MessageCallback()
def MessageCallbackWithReturnAndCustomType(credential, context):
    '''
    MC with response (this is a Saga) and use a custom type as parameter (describe in the OnStart method)

    :param CredentialInfo credential: The credential infos
    :return bool:true if user match
    '''
    Constellation.WriteInfo("Sender : %s" % context.Sender.FriendlyName)
    Constellation.WriteInfo("User=%s Password=%s" % (credential.Username, credential.Password))
    return credential.Username == credential.Password
    
@Constellation.StateObjectLink(package = "DemoPackage")
def DemoPackageSoChanged(stateObject):
    "Method called when a StateObjects of DemoPackage is updated"
    Constellation.WriteInfo("The StateObject %s pushed by %s/%s has changed ! Value = %s" % (stateObject.Name, stateObject.SentinelName, stateObject.PackageName, stateObject.Value))

def OnExit():
    pass

def OnStart():
    # Register callback on package shutdown
    Constellation.OnExitCallback = OnExit   
    
    # Write log & common properties
    Constellation.WriteInfo("Hi I'm '%s' and I currently running on %s and %s to Constellation" % (Constellation.PackageName, Constellation.SentinelName if not Constellation.IsStandAlone else 'local sandbox', "connected" if Constellation.IsConnected else "disconnected"))
    
    #  GetSetting
    Constellation.WriteInfo("Demo1 = " + str(Constellation.GetSetting("Demo1"))) # If setting not exist, return None !
    
    # Send message without parameter 
    Constellation.SendMessage("DemoPackage", "HelloWorld", [], Constellation.MessageScope.package)    
    # Send message with 2 parameter
    Constellation.SendMessage("DemoPackage", "SendMessage", [ "+33123456789", "Hi" ], Constellation.MessageScope.package)
    # Send message with complex parameter 
    Constellation.SendMessage("DemoPackage", "DemoComplex", { "A": "This is a string", "B": 123, "C": True }, Constellation.MessageScope.package)
    # Send message "MessageCallbackWithComplexeResponse" with "123" as parameter to "Demo" pasckage and write the "A" property of the response
    Constellation.SendMessageWithSaga(lambda response: Constellation.WriteInfo("A=%s" % response.A), "Demo", "MessageCallbackWithComplexResponse", 123)
    
    # Push basic StateObject
    Constellation.PushStateObject("DemoStr", "Demo de seb") # StateObject with "String" as value
    Constellation.PushStateObject("DemoBool", False, lifetime=10) # StateObject with "Bool" as value and a lifetime (10 sec here)
    Constellation.PushStateObject("DemoInt", 123, metadatas={ "DeviceId":"RPi", "Serial":"123" }) # StateObject with "Int" as value and metadatas    
    Constellation.PushStateObject("DemoFloat", 12.45, metadatas={ "DeviceId":"RPi", "Serial":"123" }, lifetime=10) # StateObject with "Float" as value, metadatas and lifetime
    
    # Custom type descriptions
    Constellation.DescribeMessageCallbackType("CredentialInfo", "Credential information", [
        { 'Name':'Username', 'Type':'string', 'Description': 'The username' },
        { 'Name':'Password', 'Type':'string', 'Description': 'The password' },
    ])
    Constellation.DescribeStateObjectType("DemoType", "Demo type", [
        { 'Name':'Sender', 'Type':'string', 'Description': 'The demo' },        
        { 'Name':'Credential', 'Type':'CredentialInfo', 'Description': 'The credential nested demo' }
    ])
    Constellation.DeclarePackageDescriptor()
    
    # Push complex StateObject
    Constellation.PushStateObject("Demo", { "Sender": "DemoPython", "Credential": { "Username": "seb", "Password":"seb" } }, "DemoType", { "DeviceId": "RPi", "Serial":"123" }) # StateObject with custom type
    
    # WriteInfo, WriteWarn & WriteError
    Constellation.WriteInfo("Hello world from Python !")
    Constellation.WriteWarn("This is a warning !")
    Constellation.WriteError("This is an error !")
    
    # Last StateObjects of the previous instance
    if Constellation.LastStateObjects:
        for so in Constellation.LastStateObjects:
            Constellation.WriteInfo(" + %s @ %s" % (so.Name, so.LastUpdate))

# Start without break ! You need to implement a "While true" even if your script stop !
# Constellation.StartAsync()
# while Constellation.IsRunning:
#     pass
#     time.sleep(1) 

# Start with embedded loop (the code after this method will newer call)
# Constellation.Start(); 

# Start by calling your custom method then embedded loop to keep your script running
Constellation.Start(OnStart);