def get_smearing_info(nproc_previous, selected_iteration, total_stack, my_dir, refinement_dir):
	global Tracker, Blockdata
	import numpy as np
	oldparamstructure           =[[], []]
	local_dict                  = {}
	for procid in range(2):
		smearing_list = []
		if( Blockdata["myid"] == Blockdata["main_node"]): lcore = read_text_file(\
		   os.path.join(my_dir, "chunk_%d.txt"%procid))
		else: lcore = 0
		lcore = wrap_mpi_bcast(lcore, Blockdata["main_node"], MPI_COMM_WORLD)	
		psize = len(lcore)
		oldparamstructure[procid] = []
		im_start, im_end   = MPI_start_end(psize, Blockdata["nproc"], Blockdata["myid"])
		local_lcore        = lcore[im_start:im_end]
		istart_old_proc_id = -1
		iend_old_proc_id   = -1
		plist              = []	
		for iproc_old in range(nproc_previous):
			im_start_old, im_end_old = MPI_start_end(psize, nproc_previous, iproc_old)
			if (im_start>= im_start_old) and im_start <=im_end_old: istart_old_proc_id = iproc_old
			if (im_end  >= im_start_old) and im_end <=im_end_old:   iend_old_proc_id   = iproc_old
			plist.append([im_start_old, im_end_old])
		ptl_on_this_cpu = im_start
		nptl_total      = 0
		for iproc_index_old in range(istart_old_proc_id, iend_old_proc_id+1):
			fout = open(os.path.join(refinement_dir,\
			   "main%03d"%selected_iteration, "oldparamstructure", \
			      "oldparamstructure_%01d_%03d_%03d.json"%(procid, \
			 iproc_index_old, selected_iteration)),'r')
			oldparamstructure_on_old_cpu = convert_json_fromunicode(json.load(fout))
			fout.close()
			mlocal_id_on_old = ptl_on_this_cpu - plist[iproc_index_old][0]
			while (mlocal_id_on_old<len(oldparamstructure_on_old_cpu)) and (ptl_on_this_cpu<im_end):
				oldparamstructure[procid].append(oldparamstructure_on_old_cpu[mlocal_id_on_old])
				local_dict [local_lcore[nptl_total]] = [Blockdata["myid"], procid, \
				   selected_iteration, nptl_total, ptl_on_this_cpu]
				ptl_on_this_cpu  +=1
				mlocal_id_on_old +=1
				nptl_total       +=1
		del oldparamstructure_on_old_cpu
		mpi_barrier(MPI_COMM_WORLD)
		
	# output number of smearing
	smearing_dict = {}
	tchunk        = []
	for procid in range(2):
		if Blockdata["myid"] == Blockdata["main_node"]:
			chunk = read_text_file(os.path.join(my_dir, "chunk_%d.txt"%procid))
			chunk_size = len(chunk)
			smearing_list =[ None for i in range(chunk_size) ]
		else: chunk_size  = 0
		chunk_size = bcast_number_to_all(chunk_size, Blockdata["main_node"], MPI_COMM_WORLD)
		local_smearing_list = []
		for im in range(len(oldparamstructure[procid])):local_smearing_list.append(len(oldparamstructure[procid][im][2]))
			
		if Blockdata["myid"] == Blockdata["main_node"]:
			im_start_old, im_end_old = MPI_start_end(chunk_size, Blockdata["nproc"], Blockdata["main_node"])
			for im in range(len(local_smearing_list)): smearing_list[im_start_old+im] = local_smearing_list[im]
		mpi_barrier(MPI_COMM_WORLD)
		if  Blockdata["myid"] != Blockdata["main_node"]:
			wrap_mpi_send(local_smearing_list, Blockdata["main_node"], MPI_COMM_WORLD)
		else:
			for iproc in range(Blockdata["nproc"]):
				if iproc != Blockdata["main_node"]:
					im_start_old, im_end_old = MPI_start_end(chunk_size, Blockdata["nproc"], iproc)
					dummy = wrap_mpi_recv(iproc, MPI_COMM_WORLD)
					for idum in range(len(dummy)): smearing_list[idum + im_start_old] = dummy[idum]
				else: pass
			write_text_file(smearing_list, os.path.join(my_dir, "smearing_%d.txt"%procid))
			for im in range(len(chunk)): smearing_dict[chunk[im]] =  smearing_list[im]
			tchunk +=chunk
		mpi_barrier(MPI_COMM_WORLD)
		
	if Blockdata["myid"] == Blockdata["main_node"]:
		tchunk.sort()
		all_smearing = np.full(len(tchunk), dtype=np.int32)
		for im in range(len(tchunk)): all_smearing[im] = smearing_dict[tchunk[im]]
	else: all_smearing
	all_smearing = wrap_mpi_gatherv(all_smearing, Blockdata["main_node"], MPI_COMM_WORLD)
	return all_smearing
	
			cdata_in_core  = (Tracker["total_stack"]*Tracker["nxinit"]*Tracker["nxinit"]*4.0)/1.e9/Blockdata["no_of_groups"]
			srdata_in_core = (Tracker["nxinit"]*Tracker["nxinit"]*np.sum(smearing_list[indx_list])*4.)/1.e9/Blockdata["no_of_groups"]
			if not Tracker["constants"]["focus3D"]:	fdata_in_core = 0.0
			else:                                   fdata_in_core = cdata_in_core
			ctfdata     = cdata_in_core
			refvol_size = (Tracker["nxinit"]*Tracker["nxinit"]*Tracker["nxinit"]*4.0*2)/1.e9 # including the 3D mask
			log_main.add( "Precalculated data (GB) in core per node (available memory per node: %6.2f):"%Tracker["constants"]["memory_per_node"])
			log_main.add( "Images for comparison: %6.2f GB; shifted images: %6.2f GB; focus images: %6.2f GB; ctfs: %6.2f GB"%\
			        (cdata_in_core, srdata_in_core, fdata_in_core, ctfdata))
			tdata = cdata_in_core+srdata_in_core+ctfdata+refvol_size
			log_main.add("The data to be in core for sorting occupies %7.3f percents of memory;  average smearing is %5.1f"%\
			    (tdata/Tracker["constants"]["memory_per_node"]*100., avg_smear))
	
	
	