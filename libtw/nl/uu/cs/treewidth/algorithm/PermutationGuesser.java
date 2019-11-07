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

import java.util.Collections;

import nl.uu.cs.treewidth.input.GraphInput.InputData;
import nl.uu.cs.treewidth.ngraph.NGraph;
import nl.uu.cs.treewidth.ngraph.NTDBag;
import nl.uu.cs.treewidth.ngraph.NVertex;
import nl.uu.cs.treewidth.ngraph.NVertexOrder;
import nl.uu.cs.treewidth.timing.Stopwatch;

public class PermutationGuesser<D extends InputData> implements UpperBound<D>, Constructive<D> {

	NGraph<D> graph;
	int upperBound = Integer.MAX_VALUE;
	NGraph<NTDBag<D>> bestDecomp;
	
	public int getUpperBound() {
		return upperBound;
	}

	public String getName() {
		return "PermutationGuesser";
	}

	public void setInput(NGraph<D> g) {
		graph = g;
	}

	public void run() {
		// Make a permutation: just add all the vertices in some order.
		NVertexOrder<D> perm = new NVertexOrder<D>();
		for( NVertex<D> v : graph ) {
			perm.order.add( v );
		}
		
		// Keep trying for a while:
		int timeLimit = 5000;
		long n = 0;
		System.out.print( "Best decomp so far: " );
		Stopwatch t = new Stopwatch();
		t.start();
		while( t.getTime()<timeLimit ) {
			
			// Try a random permutation
			Collections.shuffle( perm.order );
			
			// Turn it into a tree decomp
			PermutationToTreeDecomposition<D> algo = new PermutationToTreeDecomposition<D>(perm);
			algo.setInput( graph );
			algo.run();
			
			// See if it is better than anything we had
			if( algo.getUpperBound() < upperBound ) {
				// It is better! Remember it.
				upperBound = algo.getUpperBound();
				bestDecomp = algo.getDecomposition();
				System.out.print( " " + algo.getUpperBound() );
			} // else never mind.		
			
			++n;
			if( n%1000==0 ) System.out.print("."); 
			
		}
		t.stop();
		System.out.println();
		System.out.println( "Tried " + n + " permutations." );
	}

	public NGraph<NTDBag<D>> getDecomposition() {
		return bestDecomp;
	}

}