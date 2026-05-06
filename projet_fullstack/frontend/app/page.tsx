"use client";

import { useEffect, useState } from "react";
import api from "./api";
import toast from "react-hot-toast";
import { ActivityIcon, ArrowDownCircle, ArrowUpCircle, Plus, TrendingDown, TrendingUp, WalletIcon } from "lucide-react";

type Transactions = {
  id: string;
  text: string;
  amount: number;
  created_at: string;
}

export default function Home() {
  const [transactions, setTransactions] = useState<Transactions[]>([]);
  const [text, setText] = useState<string>("");
  const [amount, setAmount] = useState<number | "">("");

  const getTransactions = async () => {
    try {
      const response = await api.get('/transactions/');
      setTransactions(response.data);
      toast.success("Transactions récupérées avec succès !");
    } catch (error) {
      console.error(error);
      toast.error("Erreur lors de la récupération des transactions.");
    }
  };

  const handleAddTransaction = async () => {
    if (text.trim() === "" || amount === "") {
      toast.error("Veuillez remplir tous les champs.");
      return;
    }

    try {
      await api.post('/transactions/', { text, amount });
      getTransactions();
      setText("");
      setAmount("");
      toast.success("Transaction ajoutée avec succès !");
    } catch (error) {
      console.error(error);
      toast.error("Erreur lors de l'ajout de la transaction.");
    }
  }

  const handleDeleteTransaction = async (id: string) => {
    try {
      await api.delete(`/transactions/${id}/`);
      getTransactions();
      toast.success("Transaction supprimée avec succès !");

    } catch (error) {
      console.error(error);
      toast.error("Erreur lors de la suppression de la transaction.");
    }
  };

  const handleEditTransaction = async (transaction: Transactions) => {
    const newText = prompt("Entrez la nouvelle description", transaction.text);
    const newAmount = prompt("Entrez le nouveau montant", transaction.amount.toString());

    if (newText !== null && newAmount !== null) {
      try {
        const response = await api.patch(`/transactions/${transaction.id}/`, {
          text: newText,
          amount: Number(newAmount),
        });
        if (response.status === 200) {
          setTransactions(transactions.map(t => t.id === transaction.id ? response.data : t));
          toast.success("Transaction modifiée avec succès !");
        } else {
          toast.error("Erreur lors de la modification de la transaction.");
        }
      } catch (error) {
        console.error(error);
        toast.error("Erreur lors de la modification de la transaction.");
      }
    }
  };


  useEffect(() => {
    getTransactions();
  }, [])

  const amounts = transactions.map((transation: Transactions) => Number(transation.amount) || 0);
  const balance = amounts.reduce((acc, item) => (acc += item), 0) || 0;
  const income = amounts.filter((item) => item > 0).reduce((acc, item) => (acc += item), 0) || 0;
  const expense = amounts.filter((item) => item < 0).reduce((acc, item) => (acc += item), 0) || 0;

  const ratio = income === 0 ? 0 : Math.min((Math.abs(expense) / income) * 100, 100);
  return (
    <div className="w-2/3 flex flex-col gap-2">
      <div className="flex justify-between border-2 rounded-2xl border-warning/30 border-dashed bg-warning/5 p-5">

        <div className="flex flex-col items-center">
          <div className="badge badge-soft">
            <WalletIcon className="w-4 h-4" />
            <span className="ml-1 text-sm">Votre solde</span>
          </div>
          <h2 className="stat-value">
            {balance} €
          </h2>
        </div>

        <div className="flex flex-col items-center">
          <div className="badge badge-soft badge-warning">
            <ArrowDownCircle className="w-4 h-4" />
            <span className="ml-1 text-sm">Vos depanses</span>
          </div>
          <h2 className="stat-value">
            {expense} €
          </h2>
        </div>

        <div className="flex flex-col items-center">
          <div className="badge badge-soft badge-success">
            <ArrowUpCircle className="w-4 h-4" />
            <span className="ml-1 text-sm">Vos revenues</span>
          </div>
          <h2 className="stat-value">
            {income} €
          </h2>
        </div>

      </div>

      <div className="border-2 rounded-2xl border-warning/30 border-dashed bg-warning/5 p-4">

        <div className="flex justify-between items-center m-b">
          <div className="badge badge-soft badge-warning">
            <ActivityIcon className="w-4 h-4" />
            <span className="ml-1 text-sm">Ratio depanses/revenues</span>
          </div>
          <div>
            <span className="text-sm text-muted"> {ratio.toFixed(0)}% </span>
          </div>
        </div>
        <progress className="progress progress-warning" value={ratio} max="100"></progress>
      </div>
      <button className="btn w-full btn-warning" onClick={() => (document.getElementById('my_modal_2') as HTMLDialogElement).showModal()}>
        <Plus className="w-4 h-4" /> Ajouter une transaction
      </button>

      <div className="overflow-x-auto border-2 rounded-2xl border-warning/30 border-dashed bg-warning/5">
        <table className="table">
          {/* head */}
          <thead>
            <tr>
              <th>#</th>
              <th>Description</th>
              <th>Montant</th>
              <th>Date</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            {/* row 1 */}
            {transactions.map((transaction: Transactions, index: number) => (
              <tr key={transaction.id}>
                <th>{index + 1}</th>
                <td>{transaction.text}</td>
                <td >{transaction.amount > 0 ? (
                  <TrendingUp className="text-success badge badge-soft badge-success" />
                ) : (
                  <TrendingDown className="text-error badge badge-soft badge-error" />
                )} {transaction.amount} €</td>
                <td>{new Date(transaction.created_at).toLocaleDateString()}</td>
                <td className="flex gap-2">
                  <button className="btn btn-sm btn-success" onClick={() => handleEditTransaction(transaction)}>Modifier</button>
                  <button className="btn btn-sm btn-outline btn-error" onClick={() => handleDeleteTransaction(transaction.id)}>Supprimer</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>


      {/* Modal for adding */}
      <dialog id="my_modal_2" className="modal backdrop-blur-lg">
        <div className="modal-box flex flex-col gap-2">
          <h3 className="font-bold text-lg text-success text-center">Ajouter une transaction</h3>
          <form method="dialog" className="modal-backdrop">
            <input
              type="text"
              name="text"
              placeholder="Description"
              value={text}
              onChange={(e) => setText(e.target.value)}
              className="input input-success focus:border-0 w-full mb-4 placeholder:text-success text-success" required />
            <input
              type="number"
              name="amount"
              placeholder="Montant (positif pour revenu, négatif pour dépense)"
              value={amount}
              onChange={(e) => setAmount(e.target.value === "" ? "" : Number(e.target.value))}
              className="input input-success focus:border-0 w-full mb-4 placeholder:text-success text-success" required />
            <div className="modal-action">
              <button type="submit" className="btn btn-warning" onClick={() => handleAddTransaction()}>Ajouter</button>
              <button type="button" className="btn btn-outline btn-error" onClick={() => (document.getElementById('my_modal_2') as HTMLDialogElement).close()}>Annuler</button>
            </div>
          </form>
        </div>

      </dialog>

      {/* Modal for editing */}
    </div>


  );
}
