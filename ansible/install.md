1. Create directory then create venv
```bash
mkdir clab-ansible && cd clab-ansible
python3 -m venv clab-ansible
```
2. Activate the venv
```bash
source clab-ansible/bin/activate
```
3. Install ansible via pip
```bash
pip install ansible
```
4. Install arubanetworks.aoscx ansible galaxy collection
```bash
ansible-galaxy collection install arubanetworks.aoscx
```
