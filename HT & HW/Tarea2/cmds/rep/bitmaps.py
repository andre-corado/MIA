def makebm_inode(superblock, n):
    try:
        with open(superblock.path, 'rb+') as file:
            file.seek(superblock.s_bm_inode_start)
            file.read(n)
