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
import java.util.HashSet;

import nl.uu.cs.treewidth.input.GraphInput.InputData;
import nl.uu.cs.treewidth.ngraph.NGraph;
import nl.uu.cs.treewidth.ngraph.NVertex;

public class CliqueFinder< D extends InputData > {
	
	public HashSet<NVertex<D>> maxClique( NGraph<D> g ) {
		
		//System.out.println();
		
		int low = 1, high = g.getNumberOfVertices();
		
		HashSet<NVertex<D>> bestClique = null;
		int bestCliqueSize = 1;
		
		while( low<=high ) {
			
			//System.out.println( "low " + low + " high " + high );
			
			int k = (low+high)/2;
			
			//System.out.print( "Testing k=" + k + " ... ");
			
			HashSet<NVertex<D>> c = test(g,k);
			if( c == null ) {
				//System.out.print( "failed." );
				high = k-1;
			} else {
				//System.out.print( "found." );
				low = k+1;
				bestClique = c;
				bestCliqueSize = k;
			}
			
			//System.out.println();
			
		}
		
		//System.out.println();
		System.out.println( "Upperbound on clique size: " + bestCliqueSize );
		System.out.println( "Just find it within these " + bestClique.size() + " vertices." );
		return bestClique;
		
	}

	private HashSet<NVertex<D>> test( NGraph<D> g, int k ) {
		
		HashSet<NVertex<D>> potentialVertices = new HashSet<NVertex<D>>();
		
		for( NVertex<D> v : g ) {
			if( v.getNumberOfNeighbors() >= k-1 ) {
				potentialVertices.add( v );
				//System.out.println( "Potentially " + v.data.name );
			}
		}
		
		boolean changed = true;
		while( changed ) {
			changed = false;
			
			ArrayList<NVertex<D>> toBeRemoved = new ArrayList<NVertex<D>>();
			
			if( potentialVertices.size() < k ) return null;
				
			for( NVertex<D> v : potentialVertices ) {
				//System.out.println( "Checking " + v.data.name );
				int potentialCliqueNeighbors = 0;
				for( NVertex<D> n : v ) {
					if( potentialVertices.contains(n) ) ++potentialCliqueNeighbors;
				}
				//System.out.println( "It still has " + potentialCliqueNeighbors + " potential clique neighbors." );
				if( potentialCliqueNeighbors < k-1 ) {
					toBeRemoved.add( v );
					changed = true;
					//System.out.println( "Deleted " + v.data.name );
				}
			}
			
			potentialVertices.removeAll( toBeRemoved );
			
		}
		
		if( potentialVertices.size() >= k ) {
			return potentialVertices;			
		} else {
			return null;
		}
		
	}

}
