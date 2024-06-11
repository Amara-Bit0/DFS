DFS
Project Description
This project implements a simple Distributed File System (DFS) using Python. It allows users to upload files, which are then split into chunks and distributed across multiple storage nodes. Each chunk is replicated to ensure redundancy. Users can download files through a web interface built with Flask.

Features
File Upload: Upload files via a web interface.
File Splitting: Split files into smaller chunks.
Chunk Replication: Each chunk is stored on multiple storage nodes for redundancy.
File Download: Download files via a web interface by reassembling the chunks.
dfs_project/
│
├── master_node.py           # Master node managing file metadata and chunk locations
├── storage_node.py          # Storage nodes storing file chunks and handling replication
├── client.py                # Client handling file splitting, uploading, and downloading
└── web_interface/           # Flask web application for user interface
    ├── app.py               # Main Flask application file
└── README.md                # Project documentation
