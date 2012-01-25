import numpy as np
from scipy import ndimage

from openalea.image.spatial_image import SpatialImage
from openalea.image.serial.basics import imread
from openalea.container import TemporalPropertyGraph


def cellNeighbours(im, real=False, surf=False):
	"""
	calculate cell to cell dictionnary, and optionaly returns a (cell,cell) -> surface dictionnary
	real let you choose between values in voxels or values in um
	"""
	cell_cell={}
	sl=ndimage.find_objects(im2)
	xmax,ymax,zmax=im2.shape
	surface={}
	for i,j in enumerate(sl):
		if j:
			x,y,z=j
			xd=[x.start-1,x.start][x.start==0]
			xf=[x.stop+1,x.stop][x.stop==xmax-1]
			yd=[y.start-1,y.start][y.start==0]
			yf=[y.stop+1,y.stop][y.stop==ymax-1]
			zd=[z.start-1,z.start][z.start==0]
			zf=[z.stop+1,z.stop][z.stop==zmax-1]
			mlabel=im2[xd:xf,yd:yf,zd:zf].copy()
			mlabel[mlabel!=i+1]=0
			mlabel[mlabel==i+1]=1
			m=ndimage.binary_dilation(mlabel)-mlabel
			res=m*im2[xd:xf,yd:yf,zd:zf]
			l=list(np.unique(res))
			l.remove(0)
			cell_cell[i+1]=l
			for c in l:
				if real:
					surface[(i+1,c)]=len(np.where(res==c)[0])*im.resolution[0]*im.resolution[1]*im.resolution[2]
					surface[(c,i+1)]=surface[(i+1,c)]
				else:
					surface[(i+1,c)]=len(np.where(res==c)[0])
					surface[(c,i+1)]=surface[(i+1,c)]
				
	if surface:
		return cell_cell, surface
	else:
		return cell_cell, None



def toPropertyGraph(self, cell_cell=None):
	"""
	creates a PropertyGraph
	"""
	p=PropertyGraph()
	p.add_edge_property("source-target")
	if not cell_cell:
		cell_cell=cellNeighbours(self)
	for c in cell_cell.keys():
		if not p.has_vertex(c):
			p.add_vertex(c)
		for cv in cell_cell[c]:
			if not p.has_vertex(cv):
				p.add_vertex(cv)
			eid=p.add_edge(c,cv)
			p.edge_property("source-target")[eid]=(c,cv)
	return p


def SegmentedImagetoPropertyGraph(cell_cell):
	"""
	creates a PropertyGraph
	"""
	p=PropertyGraph()
	p.add_edge_property("source-target")
	for c in cell_cell.keys():
		if not p.has_vertex(c):
			p.add_vertex(c)
		for cv in cell_cell[c]:
			if not p.has_vertex(cv):
				p.add_vertex(cv)
			eid=p.add_edge(c,cv)
			p.edge_property("source-target")[eid]=(c,cv)
	return p


def createTemporalGraph(pgs, links):
	"""
	takes propertygraphs and links and create
	"""
	g = TemporalPropertyGraph()
	for k,p in enumerate(pgs):
		if not p.vertex_property("time_point"):
			p.add_vertex_property("time_point")
		for i in p.vertex():
			p.vertex_property("time_point")[i]=k			
	return g.extend(pgs,links)
	


