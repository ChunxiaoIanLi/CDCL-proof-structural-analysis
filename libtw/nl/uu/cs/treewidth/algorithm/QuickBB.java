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
import java.util.BitSet;
import java.util.HashMap;

import nl.uu.cs.treewidth.input.GraphInput.InputData;
import nl.uu.cs.treewidth.ngraph.ListGraph;
import nl.uu.cs.treewidth.ngraph.NEdge;
import nl.uu.cs.treewidth.ngraph.NGraph;
import nl.uu.cs.treewidth.ngraph.NVertex;
import nl.uu.cs.treewidth.ngraph.NVertexOrder;

/**
 * A branch and bound algorithm for treewidth, designed by Gogate and Dechter. 
 * Sometimes, this algorithm gives an exact answer (this version); 
 * sometimes the algorithm uses much time, but can be stopped to yield an 
 * upper bound on the treewidth.
 * 
 * Reference: A Complete Anytime Algorithm for Treewidth (Gogate and Dechter).
 * 
 * @author tw team 
 */
public class QuickBB< D extends InputData > implements UpperBound<D>, Permutation<D> {

	protected NGraph<QuickBBData> graph;
	private int upperbound, nodesExplored, n, skippedSets;
	private NVertexOrder<QuickBBData> permutation;
	private HashMap<BitSet,Integer> sets;
	private int branchSimps,branchASimps;
	
	final private boolean setVertexOrder = true; //Set on init
	final private boolean testSimplicialInit = true; //Test on init
	final private boolean testSimplicialBranch = false; //Test every branch step
	
	
	public QuickBB() {
		permutation = new NVertexOrder<QuickBBData>();
		upperbound = Integer.MAX_VALUE;
		sets = new HashMap<BitSet,Integer>(12000);
		nodesExplored = 0;
		skippedSets = 0;		
	}
	
	
	public int getUpperBound() {
		return upperbound;
	}

	
	public String getName() {
		return "QuickBB aka KwikBieBieDrieieie";
	}

	class QuickBBData extends InputData {
		ArrayList<NVertex<QuickBBData>>vertices = new ArrayList<NVertex<QuickBBData>>(); //vertices is used in MinorMinWidth.
		NVertex<D> original;
		public QuickBBData( NVertex<D> old) {
			super( old.data.id, old.data.name );
			original = old;			
		}
		public NVertex<D> getOriginal() { return original; }
	}
	
	class MyConvertor implements NGraph.Convertor<D,QuickBBData> {
		public QuickBBData convert( NVertex<D> old ) {
			QuickBBData d = new QuickBBData( old );
			return d;
		}
	}
	
	
	public void setInput( NGraph<D> g ) {
		graph = g.copy( new MyConvertor() );		
	}

	
	public NVertexOrder<D> getPermutation() {
		NVertexOrder<D> p = new NVertexOrder<D>( permutation.order.size() );
		for( NVertex<QuickBBData> v : permutation.order ) {
			p.order.add( v.data.getOriginal() );
		}
		return p;
	}	
	
	private class State{
		//NeighborHashSetGraph<QuickBBData> graph; //Graph
		NVertexOrder<QuickBBData> perm; //Partial order
		int g; //width of the ordering of perm along the path from the root
		int h; //lower bound on treewidth for g
		int f; //final lowerbound for this state.		
	}
	
	@SuppressWarnings("unchecked")
	public void run() {
		branchSimps = 0;
		branchASimps = 0;
	
		State s = new State();
		s.perm = new NVertexOrder<QuickBBData>();
		s.g = 0;
		
		//Run GreedyFillIn to get upperbound and init permutation
		//GreedyDegree<QuickBBData> gfi = new GreedyDegree<QuickBBData>();
		GreedyFillIn<QuickBBData> gfi = new GreedyFillIn<QuickBBData>();
		gfi.setInput(graph);
		gfi.run();				
		
		// TODO: the following is not so nice.
		// maybe make it work on other graphs someday.
		// not worth it right now.
		if(setVertexOrder) {
			if( !(graph instanceof ListGraph) ) {
				throw new UnsupportedOperationException();
			} else {
				((ListGraph<QuickBBData>)graph).vertices = gfi.getPermutation().order;
			}
		}
		n = graph.getNumberOfVertices();
		upperbound = gfi.getUpperBound();
		
		//Run MMW to get lowerbound
		MinorMinWidth_QuickBB mmw = new MinorMinWidth_QuickBB();		
		mmw.setInput(graph);		
		mmw.run();
		
		s.h = mmw.getLowerBound();
		s.f = s.h;
		
		//s.perm = gfi.getPermutation();
		permutation = gfi.getPermutation();
		
		//Debug code with information about the initial upperbound
		//System.out.println("Initial upperbound set to "+upperbound+" (with "+gfi.getName()+")");
		//System.out.println("Initial lowerbound set to "+s.h+" (with "+mmw.getName()+")");
	
		//Test is the graph contains simplicial vertices.
		if(testSimplicialInit) {
			int simps = 0;
			int asimps = 0;
			ArrayList<NVertex<QuickBBData>> simplicials = new ArrayList<NVertex<QuickBBData>>();
			for(NVertex<QuickBBData> v : graph) {
				if(graph.testSimplicial(v)) {
					simplicials.add(v);
					s.perm.order.add(v);
					++simps;
				} else if(graph.testAlmostSimplicial(v)) {
					simplicials.add(v);
					s.perm.order.add(v);
					++asimps;
				}					
			}
			//Debug information about the (almost) simplicial vertices found in the graph.
			//System.out.println("#Simplicial vertices: "+simps);
			//System.out.println("#Almost Simplicial vertices: "+asimps);
			for(NVertex<QuickBBData> simp : simplicials) {
				graph.eliminate(simp);
				s.g = Math.max(s.g, simp.getNumberOfNeighbors());
				s.f = Math.max(s.g, s.f);
			}
		}
		
		if( s.f< upperbound)
			BB(s);
		else
			System.out.println("*** No branching; treewidth found by UB en LB ***");
		
		//Information about the memorization.
		//System.out.println("# created bitsets: "+sets.size());
		//System.out.println("# skipped nodes: "+skippedSets);
		if(testSimplicialBranch) {	
			System.out.println("#Total Simplicial vertices: "+branchSimps);
			System.out.println("#Total Almost Simplicial vertices: "+branchASimps);
		}
	}
	
	
	
	@SuppressWarnings("unchecked")
	private void BB(State s) {
		nodesExplored++;
		if(graph.getNumberOfVertices()==0) {
			if(upperbound >= s.f) {
				upperbound = s.f;
				System.out.println("Setting upperbound to "+upperbound+" (no vertices left in graph)");
			}
		} else if(graph.getNumberOfVertices() < 2) {
			if(upperbound >= s.f) {
				upperbound = s.f;
				NVertexOrder<QuickBBData> permcopy = new NVertexOrder<QuickBBData>( s.perm );
				permcopy.order.add( graph.getVertex(0) );
				permutation = permcopy;
				System.out.println("Setting upperbound to "+upperbound);
			}			
		} else {
			for(int i=0; i<graph.getNumberOfVertices();++i) {			
				//Current vertex
				NVertex<QuickBBData> currentVertex = graph.getVertex(i);
								
				//Eliminate the vertex
				ArrayList<NEdge<QuickBBData>> addedEdges = graph.eliminate2(currentVertex);
											
				//Copy the current permutation
				NVertexOrder<QuickBBData> permcopy = new NVertexOrder<QuickBBData>(s.perm);
				
				//Add current vertex to the permutation
				permcopy.order.add( currentVertex );
				
				//Create a new state 
				State newS = new State();
				newS.perm = permcopy;
				newS.g = Math.max(s.g, currentVertex.getNumberOfNeighbors());
				
				//Create the bitset
				BitSet bs = getCurrentBitSet();
								
				//Run MMW to get lowerbound
				MinorMinWidth_QuickBB mmw = new MinorMinWidth_QuickBB();
				mmw.setInput(graph);
				mmw.run();
				
				//Set state values
				newS.h = mmw.getLowerBound(); 
				newS.f = Math.max(newS.g,newS.h);
				
				//Search for simplicial vertices
				ArrayList<NVertex<QuickBBData>> simplicials = new ArrayList<NVertex<QuickBBData>>();
				if(testSimplicialBranch) {					
					for(NVertex<QuickBBData> buur : currentVertex) {
						if(graph.testSimplicial(buur)) {
							simplicials.add(buur);
							graph.removeVertex(buur);
							newS.g = Math.max(newS.g, buur.getNumberOfNeighbors());
							newS.f = Math.max(newS.g, newS.f);
							permcopy.order.add(buur);
							++branchSimps;
						} else if(graph.testAlmostSimplicial(buur)) {
							simplicials.add(buur);
							graph.removeVertex(buur);
							newS.g = Math.max(newS.g, buur.getNumberOfNeighbors());
							newS.f = Math.max(newS.g, newS.f);
							permcopy.order.add(buur);
							++branchASimps;
						}
					}
				}			
				
				//Default Branch code, needed if you don't do the memorization step.
				//if(newS.f < upperbound) 
				//			BB(newS);
				
				//Check if we already have visited this branch node
				if(!sets.containsKey(bs)) {
					//We haven't, so store it
					sets.put(bs, newS.f );
					if(newS.f < upperbound) 
						BB(newS);
				} else {
					//We have, so compare the founded upperbounds
					if(sets.get(bs).intValue() > newS.f) {
						sets.put(bs,newS.f); 
						if(newS.f < upperbound) 
							BB(newS);
					} else {
						skippedSets++;
					}
				}
				
				//Restore simplicial vertices
				if(testSimplicialBranch) {
					for(NVertex<QuickBBData> simp : simplicials) {
						graph.deEliminate(simp,new ArrayList());
					}
				}
				
				//Restore graph (deeliminate current Vertex)
				graph.deEliminate(currentVertex,addedEdges);
				
				//TO_RESEARCH: This works sometimes very fast! Maybe a nice upperbound?
				//if(upperbound==newS.f)
				//	return;
			}			
		}		
	}
	
	private BitSet getCurrentBitSet() {
		BitSet bitset = new BitSet(n);
		for(NVertex<QuickBBData> v : graph) {
			bitset.set(v.data.id);
		}
		return bitset;		
	}
}
