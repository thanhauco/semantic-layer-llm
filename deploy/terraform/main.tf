# Terraform Configuration for Semantic Layer Production Infrastructure

provider "aws" {
  region = "us-west-2"
}

module "vpc" {
  source = "terraform-aws-modules/vpc/aws"
  name   = "semantic-layer-vpc"
  cidr   = "10.0.0.0/16"

  azs             = ["us-west-2a", "us-west-2b", "us-west-2c"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]

  enable_nat_gateway = true
  single_nat_gateway = false  # High Availability
}

module "eks" {
  source          = "terraform-aws-modules/eks/aws"
  cluster_name    = "semantic-layer-prod"
  cluster_version = "1.27"
  subnet_ids      = module.vpc.private_subnets
  vpc_id          = module.vpc.vpc_id

  eks_managed_node_groups = {
    api_nodes = {
      min_size     = 3
      max_size     = 10
      desired_size = 3
      instance_types = ["t3.medium"]
    }
    worker_nodes = {
      min_size     = 2
      max_size     = 5
      desired_size = 2
      instance_types = ["c5.large"] # Compute optimized for ML tasks
    }
  }
}

module "redis" {
  source = "terraform-aws-modules/elasticache/aws"
  replication_group_id = "semantic-cache"
  description          = "Redis Cluster for Semantic Layer"
  engine               = "redis"
  node_type            = "cache.r6g.large"
  num_cache_clusters   = 3
  automatic_failover_enabled = true
  multi_az_enabled     = true
  subnet_ids           = module.vpc.private_subnets
  vpc_id               = module.vpc.vpc_id
}

module "metadata_db" {
  source = "terraform-aws-modules/rds/aws"
  identifier = "semantic-metadata"
  engine     = "postgres"
  engine_version = "14"
  instance_class = "db.t4g.large"
  allocated_storage = 100
  db_name  = "semantic_meta"
  username = "admin"
  port     = 5432
  subnet_ids = module.vpc.private_subnets
  vpc_security_group_ids = [module.vpc.default_security_group_id]
  multi_az = true
}
