 proxy_set_header X-Real-IP $remote_addr; 
 proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for; 
