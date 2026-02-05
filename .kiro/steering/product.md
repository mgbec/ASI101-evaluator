# Amazon Bedrock AgentCore Samples

This repository contains samples, tutorials, and use cases for Amazon Bedrock AgentCore - a platform for deploying and operating AI agents securely at scale.

## What is Amazon Bedrock AgentCore?

Amazon Bedrock AgentCore is a framework-agnostic and model-agnostic platform that provides infrastructure services for building production-ready AI agents. It eliminates the undifferentiated heavy lifting of managing specialized agent infrastructure.

## Core Services

- **Runtime**: Serverless runtime for deploying and scaling agents and tools (any framework, any model)
- **Gateway**: Automatically converts APIs, Lambda functions, and services into MCP-compatible tools
- **Memory**: Fully-managed memory infrastructure for personalized agent experiences
- **Identity**: Seamless identity and access management across AWS and third-party applications
- **Tools**: Built-in Code Interpreter and Browser tools for secure code execution and web automation
- **Observability**: Trace, debug, and monitor agent performance with OpenTelemetry support
- **Evaluation**: Optimize agent quality with built-in and custom evaluators
- **Policy**: Fine-grained access control using Cedar policies

## Repository Purpose

This repository provides:
- Interactive tutorials for learning AgentCore fundamentals
- End-to-end use case implementations
- Framework integrations (Strands Agents, LangGraph, CrewAI, LlamaIndex, etc.)
- Infrastructure as Code templates (CloudFormation, CDK, Terraform)
- Production-ready blueprints with full-stack applications

## Key Principles

- Framework agnostic: Works with any Python-based agent framework
- Model flexible: Supports LLMs from Amazon Bedrock, OpenAI, and other providers
- Production ready: Built for enterprise workloads with security and monitoring
- Easy integration: Minimal code changes required to deploy existing agents
