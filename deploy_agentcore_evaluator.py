"""
Deploy Goal Hijack Evaluator to AgentCore

This script registers the goal hijack security evaluator as a custom
AgentCore evaluator and optionally sets up continuous monitoring.
"""

import json
import logging
import subprocess
import sys
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AgentCoreEvaluatorDeployer:
    """Deploys custom evaluator to AgentCore."""
    
    def __init__(self):
        self.evaluator_name = "goal_hijack_detector"
        self.config_file = "agentcore_goal_hijack_evaluator_config.json"
        self.online_config_name = "security_monitoring"
        self.agentcore_cmd = ["agentcore"]  # Will be set in check_prerequisites
        
    def check_prerequisites(self) -> bool:
        """Check if prerequisites are met."""
        logger.info("Checking prerequisites...")
        
        # Check if agentcore CLI is installed
        # Try the venv path first, then system path
        agentcore_paths = [
            ".venv/bin/agentcore",
            "agentcore"
        ]
        
        for cmd_path in agentcore_paths:
            try:
                result = subprocess.run(
                    [cmd_path, "--help"],
                    capture_output=True,
                    text=True,
                    check=True
                )
                logger.info(f"✓ AgentCore CLI found: {cmd_path}")
                self.agentcore_cmd = [cmd_path]
                break
            except (subprocess.CalledProcessError, FileNotFoundError):
                continue
        else:
            logger.error("✗ AgentCore CLI not found. Install with: pip install bedrock-agentcore-starter-toolkit")
            return False
        
        # Check if config file exists
        if not Path(self.config_file).exists():
            logger.error(f"✗ Configuration file not found: {self.config_file}")
            return False
        logger.info(f"✓ Configuration file found: {self.config_file}")
        
        # Check if agent is deployed
        try:
            result = subprocess.run(
                self.agentcore_cmd + ["status"],
                capture_output=True,
                text=True,
                check=True
            )
            if "agent_arn" in result.stdout or "Agent ID" in result.stdout:
                logger.info("✓ Agent deployment detected")
            else:
                logger.warning("⚠ No agent deployment found. You'll need to specify --agent-id manually.")
        except subprocess.CalledProcessError:
            logger.warning("⚠ Could not check agent status. You may need to specify --agent-id manually.")
        
        return True
    
    def list_existing_evaluators(self):
        """List existing evaluators."""
        logger.info("\n" + "=" * 80)
        logger.info("Listing existing evaluators...")
        logger.info("=" * 80)
        
        try:
            subprocess.run(
                self.agentcore_cmd + ["eval", "evaluator", "list"],
                check=True
            )
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to list evaluators: {e}")
    
    def create_evaluator(self) -> bool:
        """Create the custom evaluator."""
        logger.info("\n" + "=" * 80)
        logger.info("Creating Goal Hijack Security Evaluator...")
        logger.info("=" * 80)
        
        cmd = self.agentcore_cmd + [
            "eval", "evaluator", "create",
            "--name", self.evaluator_name,
            "--config", self.config_file,
            "--level", "TRACE",
            "--description", "ASI01 Goal Hijack Security Evaluator - Detects prompt injection, goal deviation, unauthorized tool usage, and data exfiltration attempts"
        ]
        
        logger.info(f"Running: {' '.join(cmd)}")
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            logger.info("\n✓ Evaluator created successfully!")
            logger.info(result.stdout)
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"\n✗ Failed to create evaluator")
            logger.error(f"Error: {e.stderr}")
            
            # Check if evaluator already exists
            if "already exists" in e.stderr.lower():
                logger.info("\nEvaluator already exists. You can:")
                logger.info(f"  1. Delete it: agentcore eval evaluator delete --name {self.evaluator_name}")
                logger.info(f"  2. Use it as-is for testing")
                return True
            
            return False
    
    def test_evaluator(self, agent_id: str = None, session_id: str = None) -> bool:
        """Test the evaluator with a sample session."""
        logger.info("\n" + "=" * 80)
        logger.info("Testing Goal Hijack Evaluator...")
        logger.info("=" * 80)
        
        cmd = self.agentcore_cmd + [
            "eval", "run",
            "--evaluator", self.evaluator_name
        ]
        
        if agent_id:
            cmd.extend(["--agent-id", agent_id])
        
        if session_id:
            cmd.extend(["--session-id", session_id])
        
        logger.info(f"Running: {' '.join(cmd)}")
        logger.info("\nNote: This requires an existing agent session with observability data.")
        logger.info("If you get 'No spans found', invoke your agent first and wait 2-5 minutes.\n")
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            logger.info("\n✓ Evaluation completed successfully!")
            logger.info(result.stdout)
            return True
        except subprocess.CalledProcessError as e:
            logger.warning(f"\n⚠ Evaluation test failed (this is expected if no session data exists)")
            logger.warning(f"Error: {e.stderr}")
            logger.info("\nTo test the evaluator:")
            logger.info("  1. Invoke your agent: agentcore invoke --input 'Hello'")
            logger.info("  2. Wait 2-5 minutes for CloudWatch logs to populate")
            logger.info("  3. Run: agentcore eval run --evaluator goal_hijack_detector")
            return False
    
    def setup_continuous_monitoring(self, agent_id: str = None, sampling_rate: float = 5.0) -> bool:
        """Set up continuous monitoring with online evaluation."""
        logger.info("\n" + "=" * 80)
        logger.info("Setting up Continuous Security Monitoring...")
        logger.info("=" * 80)
        
        cmd = self.agentcore_cmd + [
            "eval", "online", "create",
            "--name", self.online_config_name,
            "--sampling-rate", str(sampling_rate),
            "--evaluator", self.evaluator_name,
            "--description", "Continuous ASI01 goal hijack detection for production traffic"
        ]
        
        if agent_id:
            cmd.extend(["--agent-id", agent_id])
        
        logger.info(f"Running: {' '.join(cmd)}")
        logger.info(f"\nSampling Rate: {sampling_rate}% of interactions will be evaluated")
        logger.info("Note: Start with 5-10% for production, increase as needed.\n")
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            logger.info("\n✓ Continuous monitoring configured successfully!")
            logger.info(result.stdout)
            
            # Extract config ID from output
            for line in result.stdout.split('\n'):
                if 'Config ID:' in line:
                    config_id = line.split('Config ID:')[1].strip()
                    logger.info(f"\n📊 View results in CloudWatch:")
                    logger.info(f"   https://console.aws.amazon.com/cloudwatch/home#gen-ai-observability/agent-core")
                    logger.info(f"\n🔧 Manage configuration:")
                    logger.info(f"   agentcore eval online get --config-id {config_id}")
                    logger.info(f"   agentcore eval online update --config-id {config_id} --sampling-rate 10.0")
                    logger.info(f"   agentcore eval online delete --config-id {config_id}")
            
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"\n✗ Failed to set up continuous monitoring")
            logger.error(f"Error: {e.stderr}")
            
            if "agent" in e.stderr.lower() and "not found" in e.stderr.lower():
                logger.info("\nYou need to specify the agent ID:")
                logger.info("  agentcore eval online create \\")
                logger.info(f"    --name {self.online_config_name} \\")
                logger.info("    --agent-id <your-agent-id> \\")
                logger.info(f"    --sampling-rate {sampling_rate} \\")
                logger.info(f"    --evaluator {self.evaluator_name}")
            
            return False
    
    def print_usage_guide(self):
        """Print usage guide for the deployed evaluator."""
        logger.info("\n" + "=" * 80)
        logger.info("USAGE GUIDE")
        logger.info("=" * 80)
        
        logger.info(f"""
✅ Goal Hijack Evaluator Deployed!

EVALUATOR NAME: {self.evaluator_name}

📋 QUICK COMMANDS:

1. Run On-Demand Evaluation:
   agentcore eval run --evaluator {self.evaluator_name}

2. Evaluate Specific Session:
   agentcore eval run \\
     --evaluator {self.evaluator_name} \\
     --session-id <session-id>

3. Save Results to File:
   agentcore eval run \\
     --evaluator {self.evaluator_name} \\
     --output security_results.json

4. List Online Monitoring Configs:
   agentcore eval online list

5. View Monitoring Config Details:
   agentcore eval online get --config-id <config-id>

6. Update Sampling Rate:
   agentcore eval online update \\
     --config-id <config-id> \\
     --sampling-rate 10.0

7. Disable Monitoring Temporarily:
   agentcore eval online update \\
     --config-id <config-id> \\
     --status DISABLED

📊 VIEW RESULTS:
   CloudWatch Console → GenAI Observability → Bedrock AgentCore
   https://console.aws.amazon.com/cloudwatch/home#gen-ai-observability/agent-core

🔒 SECURITY MONITORING:
   The evaluator detects:
   - Prompt injection attacks
   - Goal deviation and hijacking
   - Unauthorized tool usage
   - Data exfiltration attempts
   - Suspicious action sequences

💡 BEST PRACTICES:
   - Start with 5-10% sampling in production
   - Monitor CloudWatch for high-risk detections
   - Set up CloudWatch alarms for risk scores < 0.3
   - Review flagged interactions regularly
   - Adjust sampling rate based on traffic volume

🔧 TROUBLESHOOTING:
   - "No spans found": Wait 2-5 minutes after agent invocation
   - "No agent specified": Add --agent-id to commands
   - "Evaluator not found": Run this script again to recreate
""")


def main():
    """Main deployment function."""
    deployer = AgentCoreEvaluatorDeployer()
    
    logger.info("=" * 80)
    logger.info("AgentCore Goal Hijack Evaluator Deployment")
    logger.info("=" * 80)
    
    # Check prerequisites
    if not deployer.check_prerequisites():
        logger.error("\n❌ Prerequisites not met. Please resolve issues and try again.")
        sys.exit(1)
    
    # List existing evaluators
    deployer.list_existing_evaluators()
    
    # Create the evaluator
    if not deployer.create_evaluator():
        logger.error("\n❌ Failed to create evaluator. See errors above.")
        sys.exit(1)
    
    # Ask if user wants to test
    logger.info("\n" + "=" * 80)
    response = input("\nWould you like to test the evaluator now? (y/n): ").strip().lower()
    if response == 'y':
        deployer.test_evaluator()
    
    # Ask if user wants to set up continuous monitoring
    logger.info("\n" + "=" * 80)
    response = input("\nWould you like to set up continuous monitoring? (y/n): ").strip().lower()
    if response == 'y':
        sampling_rate = input("Enter sampling rate (1-100, recommended 5-10 for production): ").strip()
        try:
            sampling_rate = float(sampling_rate)
            if 0 < sampling_rate <= 100:
                deployer.setup_continuous_monitoring(sampling_rate=sampling_rate)
            else:
                logger.warning("Invalid sampling rate. Skipping continuous monitoring setup.")
        except ValueError:
            logger.warning("Invalid sampling rate. Skipping continuous monitoring setup.")
    
    # Print usage guide
    deployer.print_usage_guide()
    
    logger.info("\n✅ Deployment complete!")


if __name__ == "__main__":
    main()
