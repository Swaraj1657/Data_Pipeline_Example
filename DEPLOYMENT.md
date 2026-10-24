# Deployment Guide
## Setting Up InstaMart Analytics Pipeline on a New System

This guide provides step-by-step instructions for deploying the InstaMart Advertisement & Sales Analytics Pipeline with Probabilistic Algorithms on a new system.

---

## Table of Contents

1. [System Requirements](#1-system-requirements)
2. [Prerequisites](#2-prerequisites)
3. [Installation Steps](#3-installation-steps)
4. [Configuration](#4-configuration)
5. [Running the Project](#5-running-the-project)
6. [Troubleshooting](#6-troubleshooting)
7. [Verification](#7-verification)

---

## 1. System Requirements

### 1.1 Hardware Requirements

- **RAM**: Minimum 8 GB (16 GB recommended for Docker)
- **Disk Space**: Minimum 20 GB free space
- **CPU**: 4 cores minimum (8 cores recommended)

### 1.2 Software Requirements

- **Operating System**: Windows 10/11, macOS, or Linux (Ubuntu 20.04+ recommended)
- **Docker**: Docker Desktop 4.0+ or Docker Engine 20.10+
- **Docker Compose**: v2.0+
- **Python**: 3.10 or 3.11 (for local development, optional for Docker)

### 1.3 Network Requirements

- Internet connection for downloading Docker images
- Ports 5000, 5100, 5200, 8080, 9870, 18081 should be available

---

## 2. Prerequisites

### 2.1 Install Docker

#### Windows

1. Download Docker Desktop for Windows from https://www.docker.com/products/docker-desktop
2. Run the installer with default settings
3. Enable WSL 2 backend when prompted
4. Restart your computer
5. Verify installation:
   ```powershell
   docker --version
   docker compose version
   ```

#### macOS

1. Download Docker Desktop for Mac from https://www.docker.com/products/docker-desktop
2. Install the .dmg file
3. Drag Docker to Applications folder
4. Start Docker Desktop from Applications
5. Verify installation:
   ```bash
   docker --version
   docker compose version
   ```

#### Linux (Ubuntu/Debian)

```bash
# Update package index
sudo apt-get update

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo apt-get install docker-compose-plugin

# Add user to docker group (optional, to run docker without sudo)
sudo usermod -aG docker $USER

# Verify installation
docker --version
docker compose version
```

### 2.2 Install Python (Optional, for Local Development)

#### Windows

1. Download Python 3.11 from https://www.python.org/downloads/
2. Run the installer
3. Check "Add Python to PATH"
4. Verify installation:
   ```powershell
   python --version
   pip --version
   ```

#### macOS

```bash
# Using Homebrew
brew install python@3.11

# Verify installation
python3 --version
pip3 --version
```

#### Linux

```bash
sudo apt-get update
sudo apt-get install python3.11 python3-pip

# Verify installation
python3 --version
pip3 --version
```

---

## 3. Installation Steps

### 3.1 Clone or Copy the Project

#### Option A: Clone from Git Repository (if available)

```bash
git clone <repository-url>
cd Data_Pipeline_Example
```

#### Option B: Copy Project Files

1. Copy the entire `Data_Pipeline_Example` folder to the target system
2. Navigate to the project directory:
   ```bash
   cd Data_Pipeline_Example
   ```

### 3.2 Verify Project Structure

Ensure the following structure exists:

```
Data_Pipeline_Example/
├─ README.md
├─ REPORT.md
├─ DEPLOYMENT.md
├─ ALGORITHMS.md
├─ docker-compose.batch.yml
├─ docker-compose.streaming.yml
├─ .env
├─ conf/
├─ services/
│  ├─ batch/
│  ├─ probabilistic_algorithms/
│  ├─ event-generator/
│  └─ streaming/
├─ dashboard/
├─ streaming_dashboard/
├─ algorithm_dashboard/
└─ data/
```

### 3.3 Create Required Directories

```bash
# Create data directories
mkdir -p data/input data/output hdfs/namenode hdfs/datanode checkpoints spark-events
```

**Windows PowerShell**:
```powershell
New-Item -ItemType Directory -Force -Path data\input
New-Item -ItemType Directory -Force -Path data\output
New-Item -ItemType Directory -Force -Path hdfs\namenode
New-Item -ItemType Directory -Force -Path hdfs\datanode
New-Item -ItemType Directory -Force -Path checkpoints
New-Item -ItemType Directory -Force -Path spark-events
```

---

## 4. Configuration

### 4.1 Environment Variables

Check the `.env` file for version configuration:

```env
HADOOP_VERSION=3.3.6
SPARK_VERSION=3.5.1
CONFLUENT_PLATFORM_VERSION=7.5.0
```

**Note**: These versions are tested and recommended. Modify only if necessary.

### 4.2 Docker Resource Allocation

#### Docker Desktop (Windows/macOS)

1. Open Docker Desktop
2. Go to Settings → Resources
3. Adjust settings:
   - **Memory**: 8 GB minimum (16 GB recommended)
   - **CPUs**: 4 cores minimum (8 cores recommended)
   - **Disk Image**: 60 GB minimum
4. Click "Apply & Restart"

#### Linux

Docker uses system resources by default. Ensure adequate system resources are available.

### 4.3 Network Configuration

Ensure the following ports are available (not blocked by firewall):

| Port | Service | Purpose |
|------|---------|---------|
| 5000 | Batch Dashboard | Analytics UI |
| 5100 | Streaming Dashboard | Real-time UI |
| 5200 | Algorithm Dashboard | Algorithm comparison |
| 8080 | Spark Master UI | Spark monitoring |
| 9870 | HDFS NameNode UI | HDFS monitoring |
| 18081 | Spark History Server | Spark job history |

---

## 5. Running the Project

### 5.1 Option 1: Run Algorithm Benchmarks Only (No Docker Required)

This is the quickest way to verify the probabilistic algorithms work.

#### Step 1: Install Python Dependencies

```bash
# Navigate to project directory
cd Data_Pipeline_Example

# Install dependencies (only standard library used, no external deps needed)
# No pip install required for algorithm demos
```

#### Step 2: Run Unit Tests

```bash
python services/probabilistic_algorithms/test_algorithms.py
```

Expected output: 28 tests passed

#### Step 3: Run Individual Algorithm Demos

```bash
# HyperLogLog
python services/probabilistic_algorithms/hyperloglog.py

# Count-Min Sketch
python services/probabilistic_algorithms/countmin_sketch.py

# Bloom Filter
python services/probabilistic_algorithms/bloom_filter.py

# MinHash + LSH
python services/probabilistic_algorithms/minhash_lsh.py
```

#### Step 4: Run All Benchmarks

```bash
python services/probabilistic_algorithms/run_all_benchmarks.py
```

Output saved to: `data/output/algorithm_benchmarks.json`

### 5.2 Option 2: Run with Docker (Full Pipeline)

#### Step 1: Start Docker

- **Windows/macOS**: Start Docker Desktop application
- **Linux**: Docker service should be running

Verify:
```bash
docker ps
```

#### Step 2: Build and Start Batch Stack

```bash
# Start batch pipeline with algorithm dashboard
docker compose -f docker-compose.batch.yml up --build dashboard algorithm-dashboard
```

This will:
1. Pull Docker images (Hadoop, Spark, Python)
2. Build algorithm dashboard image
3. Start HDFS (NameNode + DataNode)
4. Start Spark (Master + Workers + History Server)
5. Generate synthetic data
6. Run Spark batch job
7. Start dashboards

#### Step 3: Access Dashboards

Once services are running, access:

- **Batch Dashboard**: http://localhost:5000
- **Algorithm Dashboard**: http://localhost:5200
- **Spark Master UI**: http://localhost:8080
- **HDFS NameNode UI**: http://localhost:9870
- **Spark History Server**: http://localhost:18081

#### Step 4: Run Algorithm Benchmarks in Dashboard

1. Open http://localhost:5200
2. Click "Run Benchmarks" button
3. Wait 1-2 minutes for benchmarks to complete
4. View results and charts

#### Step 5: Stop Services

```bash
docker compose -f docker-compose.batch.yml down
```

### 5.3 Option 3: Run Streaming Pipeline

```bash
# Start streaming stack
docker compose -f docker-compose.streaming.yml up --build streaming-dashboard
```

Access:
- **Streaming Dashboard**: http://localhost:5100

Stop:
```bash
docker compose -f docker-compose.streaming.yml down
```

### 5.4 Generate Extended Synthetic Data

#### Without Docker

```bash
python services/batch/generate_extended_synthetic_data.py `
  --output data/input `
  --days 30 `
  --transactions-per-day 1000 `
  --ad-events-per-day 2000 `
  --num-customers 10000
```

**Windows PowerShell (single line)**:
```powershell
python services/batch/generate_extended_synthetic_data.py --output data/input --days 30 --transactions-per-day 1000 --ad-events-per-day 2000 --num-customers 10000
```

**Linux/macOS**:
```bash
python services/batch/generate_extended_synthetic_data.py \
  --output data/input \
  --days 30 \
  --transactions-per-day 1000 \
  --ad-events-per-day 2000 \
  --num-customers 10000
```

#### With Docker

The batch stack automatically generates data. To customize:

Edit `docker-compose.batch.yml`:
```yaml
data-generator:
  command:
    - --output
    - /opt/spark-data/input
    - --days
    - "30"
    - --transactions-per-day
    - "1000"
```

---

## 6. Troubleshooting

### 6.1 Docker Issues

#### Problem: Docker daemon not running

**Error**: `Cannot connect to the Docker daemon`

**Solution**:
- Windows/macOS: Start Docker Desktop
- Linux: `sudo systemctl start docker`

#### Problem: Insufficient memory

**Error**: Container exits with OOM (Out of Memory)

**Solution**:
- Increase Docker memory allocation in Docker Desktop Settings
- Reduce Spark executor memory in docker-compose.yml

#### Problem: Port already in use

**Error**: `bind: address already in use`

**Solution**:
- Stop conflicting services
- Or change port mapping in docker-compose.yml:
  ```yaml
  ports:
    - "5001:5000"  # Use 5001 instead of 5000
  ```

### 6.2 Python Issues

#### Problem: Module not found

**Error**: `ModuleNotFoundError: No module named 'probabilistic_algorithms'`

**Solution**:
```bash
# Ensure you're in the project root
cd Data_Pipeline_Example

# Add services to Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)/services"  # Linux/macOS
set PYTHONPATH=%PYTHONPATH%;$(pwd)\services       # Windows
```

#### Problem: Python version incompatible

**Error**: SyntaxError or import errors

**Solution**:
- Ensure Python 3.10 or 3.11 is installed
- Check version: `python --version`
- Install correct version if needed

### 6.3 Algorithm Issues

#### Problem: High error rates in Count-Min Sketch

**Explanation**: This is expected for highly skewed distributions

**Solution**:
- Use tighter epsilon (e.g., 0.001 instead of 0.01)
- Or pre-process data to reduce skew

#### Problem: Bloom Filter uses more memory than exact set

**Explanation**: This happens for small datasets due to bit array overhead

**Solution**:
- Bloom Filter benefits appear at scale (millions of items)
- For small datasets, exact set may be more efficient

### 6.4 Dashboard Issues

#### Problem: Dashboard not loading

**Solution**:
- Check if container is running: `docker ps`
- Check container logs: `docker logs algorithm-dashboard`
- Verify port mapping in docker-compose.yml

#### Problem: Benchmark results not showing

**Solution**:
- Click "Run Benchmarks" button in dashboard
- Check browser console for errors
- Verify Flask app is running: check container logs

### 6.5 Data Issues

#### Problem: No data generated

**Solution**:
- Verify data/input directory exists
- Check data-generator container logs
- Ensure directory permissions are correct

#### Problem: CSV files empty

**Solution**:
- Check generator script output for errors
- Verify parameters are valid
- Ensure sufficient disk space

---

## 7. Verification

### 7.1 Quick Verification (5 minutes)

Run these commands to verify the installation:

```bash
# 1. Check Docker
docker --version
docker compose version

# 2. Run unit tests
python services/probabilistic_algorithms/test_algorithms.py

# 3. Run one algorithm demo
python services/probabilistic_algorithms/hyperloglog.py

# 4. Generate small dataset
python services/batch/generate_extended_synthetic_data.py --output data/input --days 2 --transactions-per-day 10 --ad-events-per-day 20 --num-customers 100
```

Expected results:
- ✅ Docker versions displayed
- ✅ 28 tests passed
- ✅ HyperLogLog demo completes with results
- ✅ Data files generated in data/input

### 7.2 Full Verification (30 minutes)

#### Step 1: Run All Algorithm Demos

```bash
python services/probabilistic_algorithms/hyperloglog.py
python services/probabilistic_algorithms/countmin_sketch.py
python services/probabilistic_algorithms/bloom_filter.py
python services/probabilistic_algorithms/minhash_lsh.py
```

Expected: All demos complete successfully with benchmark results

#### Step 2: Run Comprehensive Benchmarks

```bash
python services/probabilistic_algorithms/run_all_benchmarks.py
```

Expected: JSON file created in data/output

#### Step 3: Start Docker Stack

```bash
docker compose -f docker-compose.batch.yml up --build dashboard algorithm-dashboard
```

Expected: All containers start successfully

#### Step 4: Access Dashboards

- http://localhost:5000 - Batch dashboard
- http://localhost:5200 - Algorithm dashboard

Expected: Dashboards load and display data

#### Step 5: Run Benchmarks in Dashboard

1. Open http://localhost:5200
2. Click "Run Benchmarks"
3. Wait for completion
4. View results

Expected: Benchmark results displayed with charts

### 7.3 Verification Checklist

Use this checklist to verify successful deployment:

- [ ] Docker installed and running
- [ ] Python 3.10+ installed (for local development)
- [ ] Project directories created
- [ ] Unit tests pass (28/28)
- [ ] Algorithm demos run successfully
- [ ] Synthetic data generated
- [ ] Docker images pulled/built
- [ ] Batch stack starts successfully
- [ ] Dashboards accessible
- [ ] Algorithm benchmarks complete
- [ ] Results displayed correctly

---

## 8. Performance Tuning

### 8.1 For Larger Datasets

To generate millions of records:

```bash
python services/batch/generate_extended_synthetic_data.py `
  --output data/input `
  --days 365 `
  --transactions-per-day 10000 `
  --ad-events-per-day 20000 `
  --num-customers 100000
```

This generates:
- 3.65M retail transactions
- 7.3M advertisement events
- 10.95M total records

**Note**: Ensure sufficient disk space (10+ GB) and memory (16+ GB).

### 8.2 Spark Configuration

Edit docker-compose.batch.yml to adjust Spark resources:

```yaml
spark-app:
  environment:
    - SPARK_DRIVER_MEMORY=2g
    - SPARK_EXECUTOR_MEMORY=2g
    - SPARK_EXECUTOR_CORES=2
```

### 8.3 Algorithm Parameters

For higher accuracy:

**HyperLogLog**:
```python
hll = HyperLogLog(p=14)  # More registers, lower error
```

**Count-Min Sketch**:
```python
cms = CountMinSketch(epsilon=0.0001, delta=0.001)  # Tighter bounds
```

**Bloom Filter**:
```python
bf = BloomFilter(expected_items=1000000, false_positive_rate=0.0001)
```

**MinHash + LSH**:
```python
mh = MinHash(num_permutations=256)  # More permutations
lsh = LSH(num_bands=32, rows_per_band=8)  # Higher threshold
```

---

## 9. Security Considerations

### 9.1 Docker Security

- Run Docker as non-root user when possible (Linux)
- Use specific image tags instead of `latest`
- Regularly update Docker images
- Scan images for vulnerabilities: `docker scan <image>`

### 9.2 Network Security

- Do not expose ports publicly on production systems
- Use firewall rules to restrict access
- Use HTTPS in production (not implemented in this demo)

### 9.3 Data Security

- All data is synthetic and labeled as such
- No sensitive information is generated or stored
- For production: encrypt data at rest and in transit

---

## 10. Maintenance

### 10.1 Cleanup

Remove generated data and Docker artifacts:

```bash
# Clean data
python cleanup_demo_data.py

# Clean Docker containers and volumes
docker compose -f docker-compose.batch.yml down -v
docker system prune -a
```

### 10.2 Updates

To update Docker images:

```bash
docker compose -f docker-compose.batch.yml pull
docker compose -f docker-compose.batch.yml up --build
```

### 10.3 Logs

View logs for troubleshooting:

```bash
# All services
docker compose -f docker-compose.batch.yml logs

# Specific service
docker compose -f docker-compose.batch.yml logs algorithm-dashboard
docker compose -f docker-compose.batch.yml logs spark-app
```

---

## 11. Support

### 11.1 Documentation

- **README.md**: User guide and quick start
- **REPORT.md**: Comprehensive technical report
- **ALGORITHMS.md**: Algorithm documentation
- **VERIFICATION_REPORT.md**: Verification results

### 11.2 Common Issues

Refer to the Troubleshooting section (Section 6) for common issues and solutions.

### 11.3 Getting Help

For issues not covered in this guide:
1. Check container logs: `docker compose logs`
2. Review documentation files
3. Verify system requirements
4. Check Docker resource allocation

---

## 12. Summary

This deployment guide provides complete instructions for setting up the InstaMart Analytics Pipeline on a new system. The key steps are:

1. Install Docker and Python
2. Clone/copy project files
3. Create required directories
4. Configure Docker resources
5. Run unit tests to verify
6. Start Docker stack (optional, for full pipeline)
7. Access dashboards
8. Run benchmarks

The project can run in two modes:
- **Lightweight**: Algorithm demos without Docker (Python only)
- **Full**: Complete pipeline with Docker (Hadoop, Spark, Kafka, Dashboards)

Choose the mode that fits your requirements and available resources.
