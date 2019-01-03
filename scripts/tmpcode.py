def mem_calc_and_output_info(smearing_file, log_main, nxinit):
	global Blockdata, Tracker
	from utilities import read_text_file, MPI_start_end
	import numpy as np
	# single CPU ; no info update
	smearing_list = np.array(read_text_file(smearing_file), dtype=np.int32)
	indx_list     = read_text_file(iter_id_init_file, -1)
	if len(indx_list) ==1: indx_list= indx_list[0]
	else:                  indx_list= indx_list[1]
	indx_list = np.sort(np.array(indx_list, dtype=np.int32))
	avg_smear = np.sum(smearing_list[indx_list])/indx_list.shape[0]
	cdata_in_core  = (Tracker["total_stack"]*Tracker["nxinit"]*Tracker["nxinit"]*4.0)/1.e9/Blockdata["no_of_groups"]
	srdata_in_core = (nxinit*nxinit*np.sum(smearing_list[indx_list])*4.)/1.e9/Blockdata["no_of_groups"]
	if not Tracker["constants"]["focus3D"]:	fdata_in_core = 0.0
	else:                                   fdata_in_core = cdata_in_core
	ctfdata     = cdata_in_core
	refvol_size = (nxinit*nxinit*nxinit*4.0*2)/1.e9 # including the 3D mask
	log_main.add( "Precalculated data (GB) in core per node (available memory per node: %6.2f):"%Tracker["constants"]["memory_per_node"])
	log_main.add( "Images for comparison: %6.2f GB; shifted images: %6.2f GB; focus images: %6.2f GB; ctfs: %6.2f GB"%\
			(cdata_in_core, srdata_in_core, fdata_in_core, ctfdata))
	tdata = cdata_in_core+srdata_in_core+ctfdata+refvol_size+fdata_in_core
	log_main.add("The data to be in core for sorting occupies %7.3f percents of memory;  average smearing is %5.1f"%\
		(tdata/Tracker["constants"]["memory_per_node"]*100., avg_smear))
	log_main.add("Consumed memory in sorting on individual nodes:")
	smearings_on_nodes = np.full(Blockdata["no_of_groups"], 0.0, dtype=np.float32)
	for iproc in range(Blockdata["nproc"]):
		image_start, image_end = MPI_start_end(smearing_list.shape[0], Blockdata["nproc"],iproc)
		smearings_on_nodes[iproc//Blockdata["no_of_processes_per_group"]] += \
			np.sum(smearing_list[image_start:image_end])*(nxinit*nxinit*4.)/1.e9
	msg = ""
	for icolor in range(Blockdata["no_of_groups"]):
		tdata = cdata_in_core + ctfdata + refvol_size + smearings_on_nodes[icolor]+fdata_in_core
		msg += "Node %5d :  Mem %7.2f GB  "%(icolor, tdata)+"; "
		if (icolor%3==2):
			log_main.add(msg)
			msg =""
	if Blockdata["no_of_groups"]%3!=0:log_main.add(msg)
	return