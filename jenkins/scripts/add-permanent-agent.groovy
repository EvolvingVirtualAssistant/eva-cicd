import hudson.model.*
import jenkins.model.*
import hudson.slaves.*
import hudson.slaves.EnvironmentVariablesNodeProperty.Entry
import hudson.plugins.sshslaves.verifiers.*

def agentName = "eva-jenkins-agent-1";

if(Jenkins.instance.getNode(agentName) != null) {
    return String.format("% node already exists.", agentName)
}

// Pick one of the strategies from the comments below this line
SshHostKeyVerificationStrategy hostKeyVerificationStrategy //= new KnownHostsFileKeyVerificationStrategy()
    //= new KnownHostsFileKeyVerificationStrategy() // Known hosts file Verification Strategy
    //= new ManuallyProvidedKeyVerificationStrategy("<your-key-here>") // Manually provided key Verification Strategy
    = new ManuallyTrustedKeyVerificationStrategy(false /*requires initial manual trust*/) // Manually trusted key Verification Strategy
    //= new NonVerifyingKeyVerificationStrategy() // Non verifying Verification Strategy

// Define a "Launch method": "Launch agents via SSH"
ComputerLauncher launcher = new hudson.plugins.sshslaves.SSHLauncher(
        "eva-jenkins-agent-1", // Host
        22, // Port
        "jenkins", // Credentials Id
        (String)null, // JVM Options
        (String)null, // JavaPath
        (String)null, // Prefix Start Agent Command
        (String)null, // Suffix Start Agent Command
        (Integer)null, // Connection Timeout in Seconds
        (Integer)null, // Maximum Number of Retries
        (Integer)null, // The number of seconds to wait between retries
        hostKeyVerificationStrategy // Host Key Verification Strategy
)

// Define a "Permanent Agent"
Slave agent = new DumbSlave(
        agentName,
        "/home/jenkins",
        launcher)
agent.nodeDescription = "EVA Jenkins Agent 1"
agent.numExecutors = 1
agent.labelString = agentName
agent.mode = Node.Mode.NORMAL
agent.retentionStrategy = new RetentionStrategy.Demand()

//Add env variables
//List<Entry> env = new ArrayList<Entry>();
//env.add(new Entry("key1","value1"))
//env.add(new Entry("key2","value2"))
//EnvironmentVariablesNodeProperty envPro = new EnvironmentVariablesNodeProperty(env);

//agent.getNodeProperties().add(envPro)

// Create a "Permanent Agent"
Jenkins.instance.addNode(agent)

// Update master agent to have 0 executors
def masterAgent = Jenkins.instance.getNode("master")
masterAgent.numExecutors = 0
Jenkins.instance.updateNode(masterAgent)

return String.format("% node with has been created successfully.", agentName)



