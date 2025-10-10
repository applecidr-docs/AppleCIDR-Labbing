1. Download Apache option from GoDaddy
2. Concatenate site cert and GoDaddy bundle
  A. cat domain.crt gd_bundle-g2.crt > fullchain.pem
3. SFTP the fullchain.pem file to Netbox server and save it to /etc/ssl/certs directory
4. Edit /etc/apache2/sites-available/netbox.conf
```bash
# --- snip ---
    SSLEngine on
    SSLCertificateFile /etc/ssl/certs/fullchain.pem
    SSLCertificateKeyFile /etc/ssl/private/privatekey.pem
# --- snip ---
```
5. Restart Apache
  A. sudo systemctl reload apache2.service
