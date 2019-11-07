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

import nl.uu.cs.treewidth.input.GraphInput.InputData;
import nl.uu.cs.treewidth.ngraph.NGraph;
import nl.uu.cs.treewidth.ngraph.NVertex;

/**
 * 
 * The 'minimum degree' lower bound: gives the minimum degree of a
 * vertex in the graph. [TODO Reference.]
 * 
 * @author tw team
 *
 */
public class MinDegree< D extends InputData > implements LowerBound<D> {

	protected NGraph<D> graph;
	protected int lowerbound;
	
	/**
	 * Starts out as a lowerbound of -infty; improved to the mindegree
	 * lowerbound once run() is called.
	 */
	public MinDegree() {
		lowerbound = Integer.MIN_VALUE;
	}
	
	public String getName() {
		return "MinDegree";
	}

	public void setInput( NGraph<D> g ) {
		graph = g;
	}

	public void run() {
		// just plain and simple min degree lower bound.
		
		 // initial value for finding minimum: higher than any degree
		int minDegree = graph.getNumberOfVertices();
		
		// just take minimum over edge list sizes
		for( NVertex<D> v : graph ) {
		
		//int end = minDegree;
		//for( int i=0; i<end; ++i ) {
		//	NVertex<D> v = graph.getVertex(i);
		
		//Iterator i = graph.getVertices();
		//while( i.hasNext() ) {
		//	NVertex<D> v = (NVertex<? extends InputData>) i.next();
			int degree = v.getNumberOfNeighbors();
			if( degree < minDegree ) minDegree = degree;
		}
		
		lowerbound = minDegree;
		
	}

	public int getLowerBound() {
		return lowerbound;
	}
}
