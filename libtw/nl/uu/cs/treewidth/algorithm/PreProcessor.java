/*
 * Copyright (C) 2006 
 * Thomas van Dijk
 * Jan-Pieter van den Heuvel
 * Wouter Slob
 *
 * This library is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public
 * License as published by the Free Software Foundation; either
 * version 2.1 of the License, or (at your option) any later version.
 *
 * This library is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public
 * License along with this library; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
 */
 
package nl.uu.cs.treewidth.algorithm;

import java.util.ArrayList;

import nl.uu.cs.treewidth.input.GraphInput.InputData;
import nl.uu.cs.treewidth.ngraph.NGraph;
import nl.uu.cs.treewidth.ngraph.NVertex;

/**
 * @author libtw team
 *
 * Class to perform Preprocessing on the graph.
 * Currently only simplicial and almost simplicial vertices are dealt with.
 */
public class PreProcessor<D extends InputData> implements Algorithm<D> {

	NGraph<D> graph;
	boolean doSimplicial, doAlmostSimplicial;
	int low;
	
	public PreProcessor(boolean doSimplicial, boolean doAlmostSimplicial){
		init(doSimplicial, doAlmostSimplicial);
	}
	
	public PreProcessor(){
		init(false,true);
	}
	
	private void init(boolean doSimplicial, boolean doAlmostSimplicial){
		this.doSimplicial = doSimplicial;
		this.doAlmostSimplicial = doAlmostSimplicial;
		low = 1;
	}
	
	public String getName() {
		return "Pre-process algorithms for the graph.";
	}

	public void setInput(NGraph<D> g) {
		graph = g;
	}

	public void run() {
		//Compute a lowerbound
		LowerBound<D> lbalg = new MaximumMinimumDegreePlusLeastC<D>();
		lbalg.setInput(graph);
		lbalg.run();
		low = lbalg.getLowerBound();
		System.out.println("MMD+-leastC found a lowerbound of: "+low);
		
		if (doAlmostSimplicial){
			removeAlmostSimplicial();
		} else if (doSimplicial){
			removeSimplicial();
		}
		fixids();
	}
	
	/**
	 * Removes simplicial vertices from the graph.  
	 */
	private void removeSimplicial(){
		boolean changed = true;
		while (changed){
			changed = false;
			ArrayList<NVertex<D>> simplicialVertices = new ArrayList<NVertex<D>>();
			for (NVertex<D> v: graph){
				if (graph.testSimplicial(v))
					simplicialVertices.add(v);
			}
			for (NVertex<D> v: simplicialVertices){
				low = Math.max(v.getNumberOfNeighbors(), low);
				graph.removeVertex(v);
				changed = true;
			}
		}
	}
	
	/**
	 * Removes almost simplicial vertices from the graph.
	 */
	private void removeAlmostSimplicial(){
		boolean changed = true;
		while (changed){
			changed = false;
			ArrayList<NVertex<D>> simplicialVertices = new ArrayList<NVertex<D>>();
			for (NVertex<D> v: graph){
				if (graph.testAlmostSimplicial(v) && v.getNumberOfNeighbors() <= low)
					simplicialVertices.add(v);
			}
			for (NVertex<D> v: simplicialVertices){
				low = Math.max(v.getNumberOfNeighbors(), low);
				graph.eliminate(v);
				changed = true;
			}
		}
	}
	
	/**
	 * Make sure the ids of the graph are from 1 to n 
	 */
	private void fixids(){
		int i = 0;
		for (NVertex<D> v: graph){
			v.data.id = i;
			++i;
		}
	}
	
	/**
	 * Fix the calculated treewidth by taking the maximum with the lowerbound calculated during the preprocessing.
	 * @param computedTreewidth The computed treewidth.
	 * @return The maximum of the computed treewidth and the lowerbound calculated during the preprocessing. This is the actual treewidth of the graph.
	 */
	public int fixTreewidth(int computedTreewidth){
		return Math.max(computedTreewidth, low);
	}

}
