# -*- python -*-
# -*- coding: utf-8 -*-
#
#       Topomesh : container package
#
#       Copyright or  or Copr. 2006 INRIA - CIRAD - INRA
#
#       File author(s): Jerome Chopard <jerome.chopard@sophia.inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       VPlants WebSite : https://gforge.inria.fr/projects/vplants/
#

__doc__="""
This module provide a simple pure python implementation
for a some topomesh algorithms
"""

__license__= "Cecill-C"
__revision__=" $Id$ "

from topomesh import Topomesh

###########################################################
#
#       mesh edition
#
###########################################################
def clean_remove (mesh, degree, wid) :
    """Remove a wisp and all wisps of smaller degree
    that are no longer connected to anything.
    
    :Parameters:
     - `mesh` (:class:`Topomesh`) - mesh the wisp
                                    belong to
     - `degree` (int) - degree of the wisp
     - `wid` (wid) - id of the wisp to remove in
                     the first place
    """
    to_remove = [wid]
    for deg in xrange(degree,0,-1) :
        orphans = set()
        for wid in to_remove :
            bids = tuple(mesh.borders(deg,wid) )
            mesh.remove_wisp(deg,wid)
            for bid in bids :
                if mesh.nb_regions(deg - 1,bid) == 0 :
                    orphans.add(bid)
        to_remove = orphans
    
    #handle points
    for wid in to_remove :
        mesh.remove_wisp(0,wid)
def merge_wisps (mesh, scale, wid1, wid2) :
    """
    merge two wisps into a single one
    assertion1 : wisps share a border
    assertion2 : this frontier has only these two wisps as regions
    return wid of newly created wisp
    """
    #find common frontier that will be removed
    frontier = set(mesh.borders(scale,wid1)) & set(mesh.borders(scale,wid2))
    #test assertion 1
    assert len(frontier) > 0
    #test assertion 2
    for bid in frontier :
        assert mesh.nb_regions(scale-1,bid) == 2
    #create new wisp
    nwid = mesh.add_wisp(scale)
    #connect with regions if needed
    if scale < mesh.degree() :
        for rid in set(mesh.regions(scale,wid1)) | set(mesh.regions(scale,wid2)) :
            mesh.link(scale+1,rid,nwid)
    #connect with borders
    for bid in (set(mesh.borders(scale,wid1)) | set(mesh.borders(scale,wid2))) - frontier :
        mesh.link(scale,nwid,bid)
    #remove old wisps
    clean_remove(mesh,scale,wid1)
    clean_remove(mesh,scale,wid2)
    #return
    return nwid

def is_flip_topo_allowed (mesh, eid) :
    """Test wether the given edge might be safely flipped.

    mesh: a topomesh object
    eid: id of the edge to flip
    """
    #only edge shared by two faces
    if mesh.nb_regions(1,eid) != 2 :
        return False
    #regions are triangular faces
    for fid in mesh.regions(1,eid) :
        if mesh.nb_borders(2,fid) != 3 :
            return False
    #no existing edge already between the
    #two points of the flipped edge
    pts = set()
    for fid in mesh.regions(1,eid) :
        pts.update(mesh.borders(2,fid,2))
    pid1,pid2 = pts - set(mesh.borders(1,eid))
    if pid1 in mesh.region_neighbors(0,pid2) :
        return False
    #return
    return True

def flip_edge (mesh, eid) :
    """Flip the orientation of an edge.

    in a triangulated mesh
    call is_flip_topo_allowed if there is some doubt
    on the validy of this operation
    """
    #definition of local elements
    fid1,fid2 = mesh.regions(1,eid) #work only if planar polygon
    pid3,pid4 = mesh.borders(1,eid)
    pid1, = set(mesh.borders(2,fid1,2)) - set( (pid3,pid4) )
    pid2, = set(mesh.borders(2,fid2,2)) - set( (pid3,pid4) )
    eid13, = set(mesh.borders(2,fid1)) - set(mesh.regions(0,pid3))
    eid14, = set(mesh.borders(2,fid1)) - set(mesh.regions(0,pid4))
    eid23, = set(mesh.borders(2,fid2)) - set(mesh.regions(0,pid3))
    eid24, = set(mesh.borders(2,fid2)) - set(mesh.regions(0,pid4))
    #relink eid
    mesh.unlink(1,eid,pid3)
    mesh.unlink(1,eid,pid4)
    mesh.link(1,eid,pid1)
    mesh.link(1,eid,pid2)
    #relink faces
    mesh.unlink(2,fid1,eid14)
    mesh.unlink(2,fid2,eid23)
    mesh.link(2,fid1,eid23)
    mesh.link(2,fid2,eid14)

def is_collapse_topo_allowed (mesh, eid, protected_edges) :
    """Test wether collapse of the edge is safe.

    mesh: a topomesh object
    eid: id of the edge to flip
    """
    #collapse enabled only if faces are triangle or square
    for fid in mesh.regions(1,eid) :
        if mesh.nb_borders(2,fid) not in (3,4) :
            return False
    #construct a local copy of the mesh
    #including all the faces that touch one
    #of the extremity of the edge
    #find relevant elements
    fids = set()
    for pid in mesh.borders(1,eid) :
        for bid in mesh.regions(0,pid) :
            fids.update(mesh.regions(1,bid))

    eids = set()
    pids = set()
    for fid in fids :
        eids.update(mesh.borders(2,fid))
        pids.update(mesh.borders(2,fid,2))
    elms = (pids,eids,fids)
    if mesh.degree() == 3 :
        cids = set()
        for fid in fids :
            cids.update(mesh.regions(2,fid))
        elms = elms + (cids,)
    
    #construct local mesh
    lmesh = Topomesh(mesh.degree(),"max")
    for deg,wids in enumerate(elms) :
        for wid in wids :
            lmesh.add_wisp(deg,wid)
    for deg,wids in enumerate(elms[:-1]) :
        for wid in wids :
            for rid in set(mesh.regions(deg,wid)) & elms[deg + 1] :
                lmesh.link(deg + 1,rid,wid)
    #collapse edge on this local copy
    try :
    	pid1,pid2 = collapse_edge(lmesh,eid,protected_edges)
    except UserWarning :
    	return False
    #test the result
    #edges without any face
    for wid in lmesh.wisps(1) :
        if lmesh.nb_regions(1,wid) == 0 :
            return False
    #surperposed faces
    #TODO optimization
    for ref_fid in lmesh.wisps(2) :
        ref_pids = set(lmesh.borders(2,ref_fid,2) )
        for fid in [wid for wid in lmesh.wisps(2) if wid != ref_fid] :
            pids = set(lmesh.borders(2,fid,2) )
            if len(pids) == len(ref_pids) :
                if pids == ref_pids :
                    return False
            elif len(pids) > len(ref_pids) :
                if len(pids - ref_pids) == 1 :
                    return False
            else :
                if len(ref_pids - pids) == 1 :
                    return False
    #return
    return True

def collapse_edge (mesh, eid, protected_edges) :
    """Collapse an edge.

    collapse an edge and remove adjacent faces
    face of the mesh must be triangles or quadrangles only
    return pid1, the point where edges have been reconnected
           pid2, the point that have been removed
    """
    pid1,pid2 = mesh.borders(1,eid)
    #remove face adjacents to eid
    for fid in tuple(mesh.regions(1,eid) ) :
        if mesh.nb_borders(2,fid) == 3 : #triangle to remove
            #find edge opposite to pid1
            eid1, = set(mesh.borders(2,fid)) - set(mesh.regions(0,pid1))
            #find edge opposite to pid2
            eid2, = set(mesh.borders(2,fid)) - set(mesh.regions(0,pid2))
            #test for edge protected
            if eid1 in protected_edges :
            	if eid2 in protected_edges :
            		raise UserWarning("unable to collapse edge %d on edge %d" % (eid1,eid2) )
            	else :
            		eid1,eid2 = eid2,eid1
            #remove face
            mesh.remove_wisp(2,fid)
            #relink faces connected to eid1 with eid2
            for nfid in tuple(mesh.regions(1,eid1)) :
                mesh.unlink(2,nfid,eid1)
                mesh.link(2,nfid,eid2)
            #remove eid1
            mesh.remove_wisp(1,eid1)
            #remove eid2 if necessary TODO remove lonely point too
            #if mesh.nb_regions(1,eid2) == 0 :
            #       mesh.remove_wisp(1,eid2)
    #remove eid
    mesh.remove_wisp(1,eid)
    #relink edges connected to pid2
    for neid in tuple(mesh.regions(0,pid2)) :
        mesh.unlink(1,neid,pid2)
        mesh.link(1,neid,pid1)
    #remove pid2
    mesh.remove_wisp(0,pid2)
    #return
    return pid1,pid2

def clean_duplicated_edges (mesh, eid1, eid2) :
	"""Remove a duplicated edge
	
	Remove eid2 and reconnect all faces
	to eid1. If a face is not geometrically
	defined (less than 3 edges) remove it
	too.
	
	.. warning:: eid1 and eid2 must have
	  the same borders
	
	.. warning:: do not test for cells
	
	:Returns Type: None
	"""
	faces = set(mesh.regions(1,eid2) )
	faces.discard(mesh.regions(1,eid2) )
	
	mesh.remove_wisp(1,eid2)
	
	for fid in faces :
		mesh.link(2,fid,eid1)
	
	for fid in tuple(mesh.regions(1,eid1) ) :
		if mesh.nb_borders(2,fid) < 3 :
			clean_remove(mesh,2,fid)

def collapse_edge (mesh, eid) :
	"""Collapse an edge
	
	Collapse and remove an edge
	Remove adjacent faces and
	duplicated edges if necessary
	
	.. warning::
	 - edge eid has only two borders pid1
	   and pid2
	 - there is no other edge between
	   pid1 and pid2
	
	.. warning:: do not test for cells
	
	:Parameters:
	 - `mesh` (:class:`Topomesh`)
	 - `eid` (eid) - id of edge
	    to collapse
	
	:Return:
	 - pid1, id of remaining point
	 - pid2, id of point that have been removed
	
	:Returns Type: (pid,pid)
	"""
	pid1,pid2 = mesh.borders(1,eid)
	
	#remove eid
	mesh.remove_wisp(1,eid)
	
	#relink edges connected to pid2
	for eid in tuple(mesh.regions(0,pid2) ) :
		mesh.unlink(1,eid,pid2)
		mesh.link(1,eid,pid1)
	
	mesh.remove_wisp(0,pid2)
	
	#test for duplicated edges
	edge = {}
	for eid in tuple(mesh.regions(0,pid1) ) :
		pids = tuple(mesh.borders(1,eid) )
		key = (min(pids),max(pids) )
		try :
			other_eid = edge[key]
			#edge is duplicated
			clean_duplicated_edges(mesh,other_eid,eid)
		except KeyError :
			#edge is alone for the moment
			edge[key] = eid
	
	#return
	return pid1,pid2

def collapse_face (mesh, fid) :
	"""Collapse a face
	
	remove the face and call :func:`collapse_edge`
	on all border of the face
	
	:Parameters:
	 - `mesh` (:class:`Topomesh`)
	 - `fid` (fid) - id of face
	    to collapse
	
	:Return:
	 - pid0, id of the point that stands for
	   the face
	 - pids, list of points that have been
	   removed
	
	:Returns Type: pid,list of pid
	"""
	edges = tuple(mesh.borders(2,fid) )
	
	mesh.remove_wisp(2,fid)
	
	pid0 = None
	removed_pids = []
	
	for eid in edges :
		if mesh.has_wisp(1,eid) :
			pid1,pid2 = collapse_edge(mesh,eid)
			removed_pids.append(pid2)
			pid0 = pid1
	
	return pid0,removed_pids

def clone_mesh (mesh, wids) :
	"""Clone a mesh around a set of elements
	
	Create a new mesh with the same ids
	than the old one where all wisps not
	connected to the given one are ommited.
	
	:Parameters:
	 - `mesh` (:class:`Topomesh`) - the master
	            mesh to clone
	 - `wids` (list of wid) - a list of top
	    wisps id that will remain in the clone
	
	:Returns Type: :class:`Topomesh`
	"""
	deg_max = mesh.degree()
	
	cmesh = Topomesh(deg_max,"max")
	
	#find local wisps
	loc_wisps = [(deg,tuple(mesh.borders(deg_max,wid,deg_max - deg) ) ) \
	              for deg in xrange(deg_max)] \
	           + [(deg_max,wids)]
	
	#copy wisps
	for deg,wids in loc_wisps :
		for wid in wids :
			cmesh.add_wisp(deg,wid)
	
	#copy links between wisps
	for deg,wids in loc_wisps[-1:0:-1] :
		for wid in wids :
			for bid in mesh.borders(deg,wid) :
				cmesh.link(deg,wid,bid)
	
	#return
	return cmesh

###########################################################
#
#       remove unwanted elements
#
###########################################################
def clean_geometry (mesh) :
    """
    remove wisps not geometrically defined
    i.e. with number of border smaller than scale+1
    return a list of removed elements
    """
    removed = []
    
    #remove non coherent elements
    if mesh.degree() >= 2 :
        for fid in list(mesh.wisps(2) ) :
            if mesh.nb_borders(2,fid) != len(tuple(mesh.borders(2,fid,2) ) ) :
                mesh.remove_wisp(2,fid)
                removed.append( (2,fid) )
    
    #remove undefined geometrically
    for scale in xrange(1,mesh.degree() + 1) :
        for wid in list(mesh.wisps(scale) ) :
            if mesh.nb_borders(scale,wid) < (scale + 1) :
                mesh.remove_wisp(scale,wid)
                removed.append( (scale,wid) )
    
    #return
    return removed

def clean_orphans (mesh) :
    """
    remove wisps with no regions
    return a list of removed elements
    """
    removed = []
    for scale in xrange(mesh.degree()-1,-1,-1) :
        for wid in list(mesh.wisps(scale)) :
            if mesh.nb_regions(scale,wid) == 0 :
                mesh.remove_wisp(scale,wid)
                removed.append( (scale,wid) )
    return removed

def _find_neighbor (mesh, scale, wid, wid_list) :
    """
    internal function to find a border neighbor
    of wid in the provided list of wid
    """
    for ind,eid in enumerate(wid_list) :
        if wid in set(mesh.border_neighbors(scale,eid)) :
            return ind
    raise ValueError("no neighbor find in this list")

def clean_duplicated_borders (mesh, outer = True) :
    """
    replace all wisps that account for the same
    border between two regions by a unique wisp

    if outer is True, then even elements that share
    only one region are simplified
    """
    for scale in xrange(1,mesh.degree()) :
        #find duplicated borders
        bd = {}
        for wid in mesh.wisps(scale) :
            rids = list(mesh.regions(scale,wid))
            rids.sort()
            key = tuple(rids)
            try :
                bd[key].append(wid)
            except KeyError :
                bd[key] = [wid]
        if outer :
            duplicated = [v for k,v in bd.iteritems() if len(v) > 1]
        else :
            duplicated = [v for k,v in bd.iteritems() if len(k) > 1 and len(v) > 1]
        #merge duplicates
        for wids in duplicated :
            wid1 = wids.pop(0)
            while len(wids) > 0 :
                try :
                    #find a neighbor of wid
                    ind = _find_neighbor(mesh,scale,wid1,wids)
                    wid2 = wids.pop(ind)
                    #merge wid1 and wid2
                    wid1 = merge_wisps(mesh,scale,wid1,wid2)
                except ValueError :
                    print "pb"
                    wid1 = wids.pop(0)

def clean_duplicated_borders (mesh, outer = True) :
    """
    replace all wisps that account for the same
    border between two regions by a unique wisp

    if outer is True, then even elements that share
    only one region are simplified
    """
    for deg in xrange(mesh.degree()-1,mesh.degree()-2,-1) :
        #find duplicated borders
        bd = {}
        for wid in mesh.wisps(deg) :
            rids = list(mesh.regions(deg,wid))
            rids.sort()
            key = tuple(rids)
            try :
                bd[key].append(wid)
            except KeyError :
                bd[key] = [wid]
        if outer :
            duplicated = [(k,v) for k,v in bd.iteritems() if len(v) > 1]
        else :
            duplicated = [(k,v) for k,v in bd.iteritems() if len(k) > 1 and len(v) > 1]
        #replace duplicates by a single element
        for rids,wids in duplicated :
            #create new single element
            nwid = mesh.add_wisp(deg)
            for rid in rids :
                mesh.link(deg+1,rid,nwid)
            #find external border of wids
            for bid in external_border(mesh,deg,wids) :
                mesh.link(deg,nwid,bid)
            #remove duplicates
            for wid in wids :
                clean_remove(mesh,deg,wid)

###########################################################
#
#       mesh partitioning
#
###########################################################
def expand (mesh, scale, wids) :
    """
    add a layer of wisps around a given set of wisps
    using borders to define the neighborhood
    mesh : a container.topomesh instance
    scale : the scale of wisp elements
    wisps : a list of wid
    return : a set of wid
    """
    inside_wisps = set(wids)
    for wid in wids :
        inside_wisps.update(mesh.border_neighbors(scale,wid))
    return inside_wisps

def border (mesh, scale, wids, outer = False) :
    """
    compute the outermost layer of wisps around a set of wisps
    mesh : a container.topomesh instance
    scale : the scale of wisp elements
    wids : a list of wid
    outer : a boolean that tells wether or not wisps with only one regions are considered
    return : a set of wid
    """
    inside_wisps = set(wids)
    border = set()
    for wid in wids :
        for bid in mesh.borders(scale,wid) :
            if outer and mesh.nb_regions(scale-1,bid) == 1 :
                border.add(wid)
            elif len(set(mesh.regions(scale-1,bid)) - inside_wisps) > 0 :
                border.add(wid)
    return border

def shrink (mesh, scale, wids) :
    """
    remove a layer of wisps around a set of wisps
    mesh : a container.topomesh instance
    scale : the scale of wisp elements
    wids : a list of wid
    return : a set of wid
    """
    return set(wids) - border(mesh,scale,wids)

def expand_to_border (mesh, scale, wids) :
    """
    compute the set of elements that touch the set of wisps
    mesh : a container.topomesh instance
    scale : the scale of wisp elements
    wids : a list of wid
    return : a set of wid
    """
    borders = set()
    for wid in wids :
        borders.update(mesh.borders(scale,wid))
    return borders

def expand_to_region (mesh, scale, wids) :
    """
    compute the set of elements touched by the set of wisps
    mesh : a container.topomesh instance
    scale : the scale of wisp elements
    wids : a list of wid
    return : a set of wid
    """
    cells = set()
    for wid in wids :
        cells.update(mesh.regions(scale,wid))
    return cells

def external_border (mesh, scale, wids) :
    """
    compute the list of border elements around this set of wisps
    mesh : a container.topomesh instance
    scale : the scale of wisps elements
    wids : a list of wid
    return : a set of wid
    """
    inside_wisps = set(wids)
    #compute list of borders_elms
    border_elms = expand_to_border(mesh,scale,wids)
    #remove inside borders
    border = []
    for bid in border_elms :
        regions = set(mesh.regions(scale-1,bid))
        if (len(regions) == 1) or (len(regions - inside_wisps) > 0) :
            border.append(bid)
    return border

def find_cycles (mesh, scale, length_max) :
	"""Find all cycles in the mesh.
	
	Compute the list of cycles in the mesh
	whose length is less than length_max.
	A cycle is a list of elements at the given scale
	connected by borders such as the first element
	of the cycle is connected to the last element
	
	Brut force algorithm.
	
	mesh : a container.topomesh instance
	scale : the scale to consider for cycles
	length_max : maximum number of elements in a cycle
	"""
	cycles = {}
	
	for wid in mesh.wisps(scale) :#compute all cycles from each point
		paths = [([wid],bid) for bid in mesh.borders(scale,wid)]
		for i in xrange(length_max) :#increase the size of each path
		                             #up to length_max
		    for j in xrange(len(paths) ) :#walk trough each path
				path,extr = paths.pop(0)
				neighbors = set(mesh.regions(scale - 1,extr) ) \
				            - set(path[1:])
				if len(path) == 1 :
					neighbors.remove(path[-1])
				for nid in neighbors :
					if nid == path[0] :#closed path
						pth = list(path)
						pth.sort()
						cycles[tuple(pth)] = path#necessary to not duplicate paths
					else :
						extrs = set(mesh.borders(scale,nid) )
						extrs.remove(extr)
						for bid in extrs :
							paths.append( (path + [nid],bid) )#increase the size of the path
	
	#drop keys to return only ordered paths
	return cycles.values()

