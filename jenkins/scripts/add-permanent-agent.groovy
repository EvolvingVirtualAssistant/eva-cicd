import hudson.model.*
import jenkins.model.*
import hudson.slaves.*
import hudson.slaves.EnvironmentVariablesNodeProperty.Entry
import hudson.plugins.sshslaves.verifiers.*

def getEnviron(computer) {
   def env
   def thread = Thread.start("Getting env from ${computer.name}", { env = computer.environment })
   thread.join(2000)
   if (thread.isAlive()) thread.interrupt()
   env
}

def agentAccessible(computer) {
    getEnviron(computer)?.get('PATH') != null
}

def checksAgentAndLaunchIfNeeded(Node agent) {
    def computer = agent.computer
    println "Checking computer ${computer.name}:"
    def isOK = (agentAccessible(computer) && !computer.offline)
    if (isOK) {
        println "\t\tOK, got PATH back from agent ${computer.name}."
        println('\tcomputer.isOffline: ' + computer.isOffline());
        println('\tcomputer.isTemporarilyOffline: ' + computer.isTemporarilyOffline());
        println('\tcomputer.getOfflineCause: ' + computer.getOfflineCause());
        println('\tcomputer.offline: ' + computer.offline);
    } else {
        println "  ERROR: can't get PATH from agent ${computer.name}."
        println('\tcomputer.isOffline: ' + computer.isOffline());
        println('\tcomputer.isTemporarilyOffline: ' + computer.isTemporarilyOffline());
        println('\tcomputer.getOfflineCause: ' + computer.getOfflineCause());
        println('\tcomputer.offline: ' + computer.offline);
        if (computer.isTemporarilyOffline()) {
          if (!computer.getOfflineCause().toString().contains("Disconnected by")) {
            computer.setTemporarilyOffline(false, agent.getComputer().getOfflineCause())
          }
        } else {
            computer.connect(true)
        }
    }
}

def agentName = "eva-jenkins-agent-1";

Node existingAgent = Jenkins.instance.getNode(agentName)
if(existingAgent != null) {
    println String.format("%s node already exists.", agentName)
    checksAgentAndLaunchIfNeeded(existingAgent)
    return ""
}

// Pick one of the strategies from the comments below this line
SshHostKeyVerificationStrategy hostKeyVerificationStrategy = new ManuallyTrustedKeyVerificationStrategy(false /*requires initial manual trust*/) // Manually trusted key Verification Strategy
    //= new KnownHostsFileKeyVerificationStrategy()
    //= new KnownHostsFileKeyVerificationStrategy() // Known hosts file Verification Strategy
    //= new ManuallyProvidedKeyVerificationStrategy("<your-key-here>") // Manually provided key Verification Strategy
    //= new NonVerifyingKeyVerificationStrategy() // Non verifying Verification Strategy

// Define a "Launch method": "Launch agents via SSH"
ComputerLauncher launcher = new hudson.plugins.sshslaves.SSHLauncher(
        "eva-jenkins-agent-1", // Host
        22, // Port
        "jenkins_ssh_agent1", // Credentials Id
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
agent.retentionStrategy = new RetentionStrategy.Demand(0,Long.MAX_VALUE)

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
if(masterAgent == null) {
    masterAgent = Jenkins.instance.getNode("")
}
if(masterAgent == null) {
    masterAgent = Jenkins.instance
}
masterAgent.numExecutors = 0
Jenkins.instance.updateNode(masterAgent)

checksAgentAndLaunchIfNeeded(agent)

return String.format("%s node with has been created successfully.", agentName)



