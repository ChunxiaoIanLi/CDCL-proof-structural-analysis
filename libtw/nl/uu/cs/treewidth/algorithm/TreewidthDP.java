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

import java.util.BitSet;
import java.util.HashMap;
import java.util.HashSet;

import nl.uu.cs.treewidth.input.GraphInput.InputData;
import nl.uu.cs.treewidth.ngraph.NGraph;
import nl.uu.cs.treewidth.ngraph.NVertex;

public class TreewidthDP<D extends InputData> implements Exact<D> {

	protected int treewidth, upperBound, savedDFS;
	protected NGraph<D> graph;
	protected HashMap<BitSet,Integer>[] results;
	protected int[] qvalues, visited1, oldqvalues;
	protected int[] vertex2cc, cc2q;
	protected HashSet<Integer> cStar;
	protected UpperBound<D> ubAlg;
	//protected ArrayList<Integer> changedVertices, changedValues;
	
	/**
	 * Create an instance of the DP algorithm with the trivial upperbound of n-1.
	 */
	public TreewidthDP(){
		treewidth = Integer.MAX_VALUE;
		upperBound = Integer.MAX_VALUE;
		cStar = new HashSet<Integer>();
	}
	
	/**
	 * Create an instance of the DP algorithm with a known upperbound.
	 * @param upperBound A known upperbound for the graph. 
	 */
	public TreewidthDP(int upperBound){
		treewidth = Integer.MAX_VALUE;
		this.upperBound = upperBound;
		cStar = new HashSet<Integer>();
	}
	
	/**
	 * Create an instance of the DP algorithm and use the supplied upperbound algorithm
	 * to calculate the initial upperbound.
	 * @param ubAlg The upperbound algorithm to use.
	 */
	public TreewidthDP(UpperBound<D> ubAlg){
		treewidth = Integer.MAX_VALUE;
		upperBound = Integer.MAX_VALUE;
		cStar = new HashSet<Integer>();
		this.ubAlg = ubAlg;
	}
		
	public int getTreewidth() {
		return treewidth;
	}

	public String getName() {
		return "Treewidth Dynamic Programming algorithm with upperbound and clique";
	}

	public void setInput( NGraph<D> g) {
		graph = g; // we will not destroy the graph
		if (ubAlg != null){
			ubAlg.setInput(g);
			ubAlg.run();
			upperBound = ubAlg.getUpperBound();
		}
		if (upperBound == Integer.MAX_VALUE) upperBound = graph.getNumberOfVertices() - 1;
		//TODO sort the vertexlist of the graph on data.id ascending? 
	}

	@SuppressWarnings("unchecked")
	public void run() {
		int n = graph.getNumberOfVertices();
		HashSet<Integer> c = new HashSet<Integer>();
		HashSet<Integer> p = new HashSet<Integer>();
		for (int i = 0; i < n; ++i)
			p.add(i);
		findClique(c,p);
		//System.out.println("Found clique: " +cStar);
		visited1 = new int[n];
		vertex2cc = new int[n];		
		int up = Math.max(upperBound, cStar.size()-1);
		int nrofsets = 0;
		results = new HashMap[n+1];
		results[0] = new HashMap<BitSet,Integer>();
		results[0].put(new BitSet(n),Integer.MIN_VALUE);
		//Visit the sets in increasing size
		for (int i = 1; i <= n; ++i){
			int nrsetsthissize = 0;
			int nrsetssaved = 0;
			int minTW = up;
			savedDFS = 0;
			boolean minTWChanged = false;
			//System.out.println("Starting with sets of size "+i+" with upperBound of "+up);
			results[i] = new HashMap<BitSet,Integer>(Math.max(results[i-1].size(),n));
			if (i > 2){ results[i-2] = null; }
			for (BitSet set: results[i-1].keySet()){
				if (results[i-1].get(set) < up){
					//setSet(set);
					int firstbitset = set.nextSetBit(0);
					if (firstbitset == -1){ firstbitset = n; };
					for (int j = set.nextClearBit(0); j >= 0 && j < firstbitset; j=set.nextClearBit(j+1)){
						if (!set.get(j) && !cStar.contains(j)){
							set.set(j);
							//insertInSet(set,j);
							int rPrime = computeValue(set,i);
							if (rPrime >= n-i-1 && rPrime < minTW){
								minTW = rPrime;
								minTWChanged = true;
							}
							BitSet toStore = (BitSet) set.clone();
							if (rPrime < up){
								//This set can possibly improve the upperbound
								if (results[i].containsKey(toStore)){
									rPrime = Math.min(results[i].get(set),rPrime);
								}
								results[i].put(toStore,rPrime);
								++nrsetssaved;
							}
							set.clear(j);
							//revertSet();
							++nrsetsthissize;
						}
					}
				}
			}
			//System.out.println("Examined "+nrsetsthissize+" sets of which "+nrsetssaved+" were saved in the HashMap and savedDFS: " + savedDFS);
			nrofsets += nrsetsthissize;
			if (minTWChanged){
				up = Math.min(up, Math.max(minTW,n-i-1));
			} else if (results[i].size() != 0) {
				up = Math.min(up, n-i-1);
			}
		}
		if (results[n].values().toArray().length > 0)
			treewidth = (Integer) results[n].values().toArray()[0];
		else
			treewidth = up;
		treewidth = Math.max(treewidth, cStar.size()-1);
		//System.out.println("Total nr of sets: "+nrofsets);
		
	}

	/**
	 * Computes the value for a set in the DP-table.
	 * @param set The set of vertices.
	 * @param size The number of vertices in the set.
	 * @return The value for a set in the DP-table.
	 */
	private int computeValue(BitSet set, int size){
		int minValue = Integer.MAX_VALUE;
		//int vertexId;
		setSet(set,size);
		//For all vertices in the set
		for (int i = set.nextSetBit(0); i >= 0; i=set.nextSetBit(i+1)){
			//remove the vertex from the set
			set.clear(i);
			//If the remaining set of vertices could still contribute to a better upperbound
			if (results[size-1].containsKey(set)){
				int prevTW = results[size-1].get(set);
				//int q = q(set,new boolean[graph.vertices.size()],i);
				//int thisTW = Math.max(prevTW,q);
				int thisTW = Math.max(prevTW,cc2q[vertex2cc[i]]);
				if (thisTW < minValue){
					minValue = thisTW;
					//vertexId = i;
				}
			}
			//put the vertex back in the set
			set.set(i);
		}
		//System.out.print(" Computed value: "+minValue+"\n");
		return minValue;
	}
	
	/**
	 * Sets the correct q-values for the connected components in the set.
	 * @param set The set of vertices.
	 * @param size The size of the set.
	 */
	private void setSet(BitSet set, int size){
		//compute q-values for the connected components
		//changedVertices = new ArrayList<Integer>();
		//changedValues = new ArrayList<Integer>();
		//qvalues = new int[graph.vertices.size()];
		int n = graph.getNumberOfVertices();
		for(int i = 0; i < n; ++i){
			visited1[i] = 0;
			vertex2cc[i] = 0;
		}
		//visited1 = new int[graph.vertices.size()];
		//vertex2cc = new int[graph.vertices.size()];
		cc2q = new int[size+1];
		int start = 0;
		int cc = 0;
		boolean done = false;
		while (!done){
			int bit = set.nextSetBit(start);
			if (bit == -1){
				done = true;
			} else if (visited1[bit] == 0) {
				++cc;
				cc2q[cc] = computeQValue(set,bit,visited1,cc);
			}
			start = bit+1;
		}
	}
	
	/*
	 * Currently not used 
	private void insertInSet(BitSet set, int vertex){
		//check if neighbors are in the set
		oldqvalues = qvalues.clone();
		NVertex<D> v = graph.getVertex(vertex);
		boolean visitedNeighbor = false;
		int neighborInSet = Integer.MIN_VALUE;
		for (NVertex<D> n: v){
			int neighbor = n.data.id;
			if (set.get(neighbor)){
				neighborInSet = neighbor;
			} else if (visited1[neighbor] != 0){
				visitedNeighbor = true;
			}
		}
		if (neighborInSet == Integer.MIN_VALUE){
			//changedVertices.add(vertex);
			//changedValues.add(qvalues[vertex]);
			qvalues[vertex] = v.getNumberOfNeighbors();
			++savedDFS;
		} else if (!visitedNeighbor){
			setQValues(set, vertex, new boolean[graph.getNumberOfVertices()], qvalues[neighborInSet]+v.getNumberOfNeighbors(), true);
			++savedDFS;
		} else {
			// doe maar DFS
			int newq = computeQValue(set,vertex,new int[graph.getNumberOfVertices()],1);
			setQValues(set, vertex, new boolean[graph.getNumberOfVertices()], newq, true);
		}
	}
	*/
	
	/*
	 * Currently not used
	private void revertSet(){
		
		for (int i = 0; i < changedVertices.size(); ++i){
			int vertex = changedVertices.get(i);
			int value = changedValues.get(i);
			qvalues[vertex] = value;
		}
		
		qvalues = oldqvalues;
	}
	*/
	
	/**
	 * Computes the Q-value for a vertex (and the whole connected component).
	 * @param set The set of vertices currently considered.
	 * @param vertex The vertex to compute the Q-value for.
	 * @param visited An array of integers that maps the vertices to the id of the connected component. 
	 * @param cc The id of the connected component of the vertex.
	 * @return The computed Q-value.
	 */
	private int computeQValue(BitSet set, int vertex, int[] visited, int cc){
		int q = 0;
		visited[vertex] = cc;
		vertex2cc[vertex] = cc;
		for (NVertex<D> neighborv: graph.getVertex(vertex) ){
			int neighbor = neighborv.data.id;
			if (visited[neighbor] != cc){
				if (set.get(neighbor)){
					q = q + computeQValue(set,neighbor,visited,cc);
				} else {
					visited[neighbor] = cc;
					++q;
				}
			}
			/*
			if (!set.get(neighbor) && visited[neighbor] != cc){
				visited[neighbor] = cc;
				++q;
			} else if (set.get(neighbor) && visited[neighbor] != cc){
				q = q + computeQValue(set,neighbor,visited,cc);
			}*/
		}
		return q;
	}
	
	/*
	 * Currently not used 
	private void setQValues(BitSet set, int vertex, boolean[] visited, int qValue, boolean saveChanges){
		visited[vertex] = true;
		//if (saveChanges){
		//	changedVertices.add(vertex);
		//	changedValues.add(qvalues[vertex]);
		//}
		qvalues[vertex] = qValue;
		for (NVertex<D> neighborv: graph.getVertex(vertex) ){
			int neighbor = neighborv.data.id;
			if (set.get(neighbor) && !visited[neighbor]){
				setQValues(set,neighbor,visited,qValue, saveChanges);
			}
		}
		//System.out.println("Q: " +qValue);
	}
	*/
	
	/*
	 * initial method to calculate the q-value.
	private int q(BitSet set, boolean[] visited, int v){
		int sizeW = 0;
		visited[v] = true;
		for (NeighborHashSetVertex<InputData> neighborv: graph.vertices.get(v).neighbors){
			int neighbor = neighborv.data.id;
			if (!set.get(neighbor) && !visited[neighbor]){
				visited[neighbor] = true;
				++sizeW;
			} else if (set.get(neighbor) && !visited[neighbor]){
				sizeW = sizeW + q(set, visited, neighbor);
			}
		}
		////System.out.println("Q: " +sizeW);
		return sizeW;
	}*/
	
	
	@SuppressWarnings("unchecked")
	//Finds the maximum clique.
	private void findClique(HashSet<Integer> c, HashSet<Integer> p){
		if (c.size() > cStar.size()){
			cStar = c;
		}
		if (c.size()+p.size() > cStar.size()){
			HashSet<Integer> pIt = (HashSet<Integer>) p.clone();
			for(int v: pIt){
				p.remove(v);
				HashSet<Integer> cPrime = (HashSet<Integer>) c.clone();
				cPrime.add(v);
				HashSet<Integer> pPrime = (HashSet<Integer>) p.clone();
				for (int n: p)
					//if (!graph.vertices.get(v).neighbors.contains(graph.vertices.get(n)))
					if( !graph.getVertex(v).isNeighbor( graph.getVertex(n) ) )
						pPrime.remove(n);
				findClique(cPrime,pPrime);
			}
		}
	}
}
